from pydantic import Field, RedisDsn
from config.setting_config import Settings


class RedisConfig(Settings):
    redis_host: str = Field(default='localhost')
    redis_port: int = Field(default=6379)
    redis_password: str
    redis_database: int = Field(default=0)

    @property
    def url(self):
        return str(RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
            path=f"{self.redis_database}",
        ))
