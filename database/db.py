from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database_config import DbConfig


class Db:
    def __init__(self, config : DbConfig):
        self._engine = create_engine(config.url)
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()

    @property
    def session(self):
        return self._session