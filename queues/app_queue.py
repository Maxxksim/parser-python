import os
import signal
import time
from config.queue_config import QueueConfig
from controller.parsed_data_controller import ParsedDataController
from database.rd import Rd
from parsing.parser import Parser


class Queue:
    DEFAULT_PROCESS: int = 1


    def __init__(self, config: QueueConfig, parser: Parser, redis: Rd, controller: ParsedDataController):
        self._number_processes: int = config.number_processes
        self._should_stop: bool = False
        self._processes: list = []
        self._parser: Parser = parser
        self._redis: Rd = redis
        self._controller: ParsedDataController = controller

        signal.signal(signal.SIGTERM, self.__handler)
        signal.signal(signal.SIGINT, self.__handler)
        signal.signal(signal.SIGHUP, self.__handler)

    def __handler(self, signum, frame) -> None:
        self._should_stop = True
        for pid in list(self._processes):
            os.kill(pid, signal.SIGTERM)

    def start(self) -> None:
        self.__move_links_to_queue()
        # self._parser.fill_queue()

        for i in range(self.__get_number_processes()):
            self._processes.append(self.__create_process('parsing'))

        self._processes.append(self.__create_process('saving'))

        while self._processes:
            pid, status = os.wait()
            self._processes.remove(pid)

    def __create_process(self, processes_type) -> int:
        pid = os.fork()

        if pid == 0:
            self._processes = []

            if processes_type == 'parsing':
                parser = self._parser.get_new_instance()
                parser.start_parsing_links()

            elif processes_type == 'saving':
                redis_client = self._redis.get_client()

                while not self._should_stop:

                    if (
                            redis_client.llen("queue") == 0 and
                            redis_client.llen("queue:parsed:data") == 0 and
                            redis_client.llen("queue:processing") == 0
                    ):
                        break

                    if not (parsed_data := redis_client.brpop('queue:parsed:data', 30)):
                        continue

                    try:
                        link = self._controller.save_data(parsed_data[1])
                        pipe = redis_client.pipeline(transaction=True)
                        pipe.srem('set:processing', link)
                        pipe.lrem('queue:processing', 1, link)
                        pipe.execute()
                    except RuntimeError:
                        redis_client.lpush('queue:parsed:data', parsed_data[1])
            os._exit(0)

        return pid

    def __get_number_processes(self) -> int:
        if self._number_processes <= 0:
            return self.DEFAULT_PROCESS

        return self._number_processes

    def __move_links_to_queue(self):
        redis_client = self._redis.get_client()
        count = redis_client.llen('queue:processing')

        for _ in range(count):
            redis_client.lmove('queue:processing', 'queue', 'RIGHT', 'LEFT')
