import os 
from dotenv import load_dotenv

from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    DB_URL_SYNC: str = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost:3306/{os.getenv('DB_NAME')}"
    DBBaseModel: ClassVar = declarative_base()
    
    class Config:
        case_sensitive = True
    
settings: Settings = Settings()