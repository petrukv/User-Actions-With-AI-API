from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        extra = 'allow'

    APP_HOST_PORT: int
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    
settings = Settings()