from sqlalchemy import Text
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_bin',
    }

    type_annotation_map = {
        str: Text
    }
