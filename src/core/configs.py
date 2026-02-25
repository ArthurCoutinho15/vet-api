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
    
    JWT_SECRET: str = str(os.getenv('JWT_SECRET'))
    ALGORITHM: str = 'HS256'
    
    # 60 minutos * 24 horas * 7 dias = 1 semana em minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    class Config:
        case_sensitive = True
    
settings: Settings = Settings()