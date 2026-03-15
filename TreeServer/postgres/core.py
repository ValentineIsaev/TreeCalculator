from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .configs import postgres_settings


engine = create_async_engine(url=postgres_settings.POSTGRES_URL)

session_factory = async_sessionmaker(engine, class_=AsyncSession)