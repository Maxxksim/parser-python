import logging
import sys
from config.logger_config import LoggerConfig


class Logger:
    name: str = "Parser"
    LOG_LEVEL: int = logging.DEBUG

    def __init__(self, config: LoggerConfig) -> None:
        self.__logger = logging.getLogger(self.name)
        self.__logger.setLevel(self.LOG_LEVEL)
        self.__config = config

        handler = self.__create_handler(self.__config.logs_path)
        handler.setLevel(self.LOG_LEVEL)
        handler.setFormatter(logging.Formatter())

        self.__logger.addHandler(handler)
        self.__logger.propagate = False

    def __create_handler(self, logs_path : str) -> logging.Handler:
        if self.__config.log_mode == 'file':
            return logging.FileHandler(logs_path)

        return logging.StreamHandler(sys.stdout)

    @property
    def log(self):
        return self.__logger

    @property
    def log_mode(self):
        return self.__config.log_mode

    @property
    def logs_path(self):
        return self.__config.logs_path