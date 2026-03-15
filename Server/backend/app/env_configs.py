from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / '.env', extra='ignore')


class HttpSettings(Base):
    TREE_BASE_HTTP_URL: str

    SELF_URL: str
    SELF_PORT: int
