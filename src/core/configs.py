import os 
from dotenv import load_dotenv

from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"mysql+aiomysql://{str(os.getenv('USER'))}:{str(os.getenv('PASS'))}@localhost:3306/veterinaria"
    DB_URL_SYNC: str  = f"mysql+pymysql://{str(os.getenv('USER'))}:{str(os.getenv('PASS'))}@localhost:3306/veterinaria"
    DBBaseModel: ClassVar = declarative_base()
    
    class Config:
        case_sensitive = True
    
settings: Settings = Settings()