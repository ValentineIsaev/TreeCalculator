from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

print(Path(__file__).parent / '.env')
class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / '.env', extra='ignore')

    POSTGRES_URL: str

postgres_settings = PostgresSettings()