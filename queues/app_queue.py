import os
import signal
import time
from config.queue_config import QueueConfig
from database.rd import Rd
from parsing.parser import Parser


class Queue:

    def __init__(self, config: QueueConfig, parser: Parser, redis: Rd):
        self._numberProcesses: int = config.number_processes
        self._shouldStop: bool = False
        self._processes: list = []
        self._parser = parser
        self._redis = redis

        signal.signal(signal.SIGTERM, self.__handler)
        signal.signal(signal.SIGINT, self.__handler)
        signal.signal(signal.SIGHUP, self.__handler)

    def __handler(self, signum, frame) -> None:
        self._shouldStop = True
        for pid in list(self._processes):
            os.kill(pid, signal.SIGTERM)

    def start(self) -> None:
        for _ in range(self._numberProcesses):
            self._processes.append(self.__create_process())

        while self._processes:
            pid, status = os.wait()
            self._processes.remove(pid)

            if not self._shouldStop:
                self._processes.append(self.__create_process())


    def __process(self, link: str) -> None:
        self._parser.parse(link)

    def __create_process(self) -> int:
        pid = os.fork()

        if pid == 0:
            self._processes = []
            redis_client = self._redis.get_client()

            try:

                while not self._shouldStop:
                    link = redis_client.blmove(
                        'queue', 'queue:processing', timeout=30, src='RIGHT', dest='LEFT',
                    ).decode()

                    if link is None:
                        continue

                    print(f"Process {os.getpid()} started: {link}")
                    self.__process(link)
                    redis_client.lrem('queue:processing', 1, link)
                    print(f"Process {os.getpid()} ended: {link}")
            finally:
                os._exit(0)

        return pid
