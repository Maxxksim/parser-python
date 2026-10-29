from pydantic import Field
from sqlalchemy import URL

from config.setting_config import Settings


class DbConfig(Settings):
    db_driver: str = Field(default='mysql+pymysql')
    db_host: str = Field(default='localhost')
    db_port: int = Field(default=3306)
    db_username: str
    db_password: str
    db_database: str

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.db_driver,
            username=self.db_username,
            host=self.db_host,
            port=self.db_port,
            database=self.db_database,
        )
