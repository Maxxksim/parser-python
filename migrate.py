from sqlalchemy import create_engine
from config.app_config import Config
from models import BaseModel

try:
    engine = create_engine(Config().db.url)
    BaseModel.metadata.create_all(engine)
    print("Migrations have been migrated.")
except Exception as e:
    print(f"DATABASE ERROR: {e}")