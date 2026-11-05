import os
import signal
from Logs.logger import Logger
from config.queue_config import QueueConfig
from controller.parsed_data_controller import ParsedDataController
from database.rd import Rd
from parsing.parser import Parser


class Queue:
    DEFAULT_PROCESS: int = 1

    def __init__(self, config: QueueConfig, parser: Parser, redis: Rd, controller: ParsedDataController,
                 logger: Logger):
        self.__number_processes: int = config.number_processes

        self.__should_stop: bool = False
        self.__processes: list = []
        self.__parser: Parser = parser
        self.__redis: Rd = redis
        self.__controller: ParsedDataController = controller
        self.__logger: Logger = logger

        signal.signal(signal.SIGTERM, self.__stop_handler)
        signal.signal(signal.SIGINT, self.__stop_handler)
        signal.signal(signal.SIGHUP, self.__stop_handler)

    def __stop_handler(self, signum, frame) -> None:
        self.__logger.log.info("QUEUE MESSAGE (STOP): start stoping processes.")
        self.__should_stop = True

        for pid in list(self.__processes):
            os.kill(pid, signal.SIGTERM)

    def start(self) -> None:
        """
        Run processes for filling queue, parsing and saving links
        and cycle which waits for closing parsing, saving processes.

        :return: None
        """
        self.__move_links_to_queue()

        pid_filling_queue_process = self.__create_process('filling_queue')
        self.__processes.append(pid_filling_queue_process)
        self.__logger.log.info(
            'QUEUE MESSAGE (PROCESS): filling queue process with PID: %s has been started.',
            pid_filling_queue_process,
        )

        os.waitpid(pid_filling_queue_process, 0)
        self.__processes.remove(pid_filling_queue_process)
        self.__logger.log.info(
            'QUEUE MESSAGE (PROCESS): filling queue process with PID: %s has been done.',
            pid_filling_queue_process,
        )

        if self.__should_stop:
            self.__logger.log.info("QUEUE MESSAGE (STOP): parser has been stopped before main parsing.")
            return

        for i in range(self.__get_number_processes()):
            self.__processes.append(pid := self.__create_process('parsing'))
            self.__logger.log.info('QUEUE MESSAGE (PROCESS): parsing process with PID: %s has been started.', pid)


        self.__processes.append(pid := self.__create_process('saving'))
        self.__logger.log.info('QUEUE MESSAGE (PROCESS): saving process with PID: %s has been started.', pid)

        while self.__processes:
            pid, status = os.wait()
            self.__processes.remove(pid)
            self.__logger.log.info("QUEUE MESSAGE (PROCESS): process with PID %s has done.", pid)

    def __create_process(self, processes_type) -> int:
        pid = os.fork()

        if pid == 0:
            self.__processes = []

            if processes_type == 'parsing':
                parser = self.__parser.get_new_instance()
                parser.start_parsing_links()

            elif processes_type == 'saving':
                redis_client = self.__redis.get_client()

                while not self.__should_stop or redis_client.llen("queue:processing") > 0:

                    if (
                            redis_client.llen("queue") == 0 and
                            redis_client.llen("queue:parsed:data") == 0 and
                            redis_client.llen("queue:processing") == 0
                    ):
                        break

                    if not (parsed_data := redis_client.brpop('queue:parsed:data', 30)):
                        continue

                    try:
                        link = self.__controller.save_data(parsed_data[1])
                        pipe = redis_client.pipeline(transaction=True)
                        pipe.srem('set:processing', link)
                        pipe.lrem('queue:processing', 1, link)
                        pipe.execute()
                    except RuntimeError as error:
                        redis_client.lpush('queue:parsed:data', parsed_data[1])
                        self.__logger.log.error("QUEUE MESSAGE (SAVING): Error: %s.", error)
            elif 'filling_queue':
                parser = self.__parser.get_new_instance()
                parser.fill_queue()

            os._exit(0)
        return pid

    def __get_number_processes(self) -> int:
        if self.__number_processes <= 0:
            return self.DEFAULT_PROCESS

        return self.__number_processes

    def __move_links_to_queue(self):
        redis_client = self.__redis.get_client()
        count = redis_client.llen('queue:processing')

        self.__logger.log.info("QUEUE MESSAGE (MOVING LINKS): start")

        for _ in range(count):
            redis_client.lmove('queue:processing', 'queue', 'RIGHT', 'LEFT')

        self.__logger.log.info("QUEUE MESSAGE (MOVING LINKS): %s links have been moved.", count)
