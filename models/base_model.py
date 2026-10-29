from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_bin',
    }
