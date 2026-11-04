from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database_config import DbConfig


class Db:
    def __init__(self, config : DbConfig):
        self.__engine = create_engine(config.url)
        self.__session_maker = sessionmaker(bind=self.__engine)
        self.__session = self.__session_maker()

    @property
    def connection(self):
        return self.__session