import os
import random
import signal
import time

from Config.Config import Config

class Queue:

    def __init__(self, config : Config):
        self._numberProcesses : int = config.NUMBER_PROCESSES
        self._shouldStop : bool = False
        self._processes : list = []

        signal.signal(signal.SIGTERM, self.__handler)
        signal.signal(signal.SIGINT, self.__handler)
        signal.signal(signal.SIGHUP, self.__handler)

    def __handler(self, signum, frame) -> None:
        self._shouldStop = True

    def start(self) -> None:
        for i in range(self._numberProcesses):
            pid = os.fork()

            if pid == 0:

                while not self._shouldStop:
                    print(f"Process with pid {os.getpid()} has started parsing")
                    self.__process(os.getpid())
                    print(f"Process with pid {os.getpid()} has ended parsing")
                os._exit(0)
            self._processes.append(pid)

        while self._processes:
            pid, status = os.wait()
            self._processes.remove(pid)
            print(f"Process with pid {pid} has been done")

    @staticmethod
    def __process(pid) -> None:
        print(f"Process with pid {pid} is parsing...")
        time.sleep(random.randrange(1, 15))