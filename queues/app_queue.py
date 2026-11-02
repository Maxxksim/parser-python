import os
import signal
import time
from config.queue_config import QueueConfig
from controller.parsed_data_controller import ParsedDataController
from database.rd import Rd
from parsing.parser import Parser


class Queue:

    def __init__(self, config: QueueConfig, parser: Parser, redis: Rd, controller: ParsedDataController):
        self._numberProcesses: int = config.number_processes
        self._shouldStop: bool = False
        self._processes: list = []
        self._parser = parser
        self._redis = redis
        self._controller = controller

        signal.signal(signal.SIGTERM, self.__handler)
        signal.signal(signal.SIGINT, self.__handler)
        signal.signal(signal.SIGHUP, self.__handler)

    def __handler(self, signum, frame) -> None:
        self._shouldStop = True
        for pid in list(self._processes):
            os.kill(pid, signal.SIGTERM)

    def start(self) -> None:

        for i in range(self._numberProcesses):
            self._processes.append(self.__create_process('parsing'))

            if i == self._numberProcesses - 1:
                self._processes.append(self.__create_process('saving'))

        while self._processes:
            pid, status = os.wait()
            self._processes.remove(pid)

    def __create_process(self, processes_type) -> int:
        pid = os.fork()

        if pid == 0:
            self._processes = []

            while not self._shouldStop:
                if processes_type == 'parsing':
                    self._parser.parse()
                elif processes_type == 'saving':
                    redis_client = self._redis.get_client()

                    if not (parsed_data := redis_client.brpop('queue:parsed:data', 30)):
                        continue
                    link = self._controller.save_data(parsed_data[0])
                    redis_client.srem('set:processing', link)
                    redis_client.lrem('queue:processing', 1, link)

            self._processes.append(pid)
            os._exit(0)

        return pid
