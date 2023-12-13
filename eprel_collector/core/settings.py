from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    )
    logging_dir: str = str(BASE_DIR / 'logs')
    pdfs_dir: str = str(BASE_DIR / 'pdfs')
    eprel_maximum_connections: int = 200
    eprel_id_min: int = 1
    eprel_id_max: int = 2_000_000
    re_read_attempts: int = 5
    pause_between_attempts: int = 4
    http_timeout: int = 30


settings = Settings()
