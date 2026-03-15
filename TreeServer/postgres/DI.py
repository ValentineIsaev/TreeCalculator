from .core import session_factory

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import RootsRepository, TreesRepository, SoilsRepository

def get_db_session():
    session = session_factory()
    yield session
    session.close()

def root_repo(session: AsyncSession = Depends(get_db_session)):
    return RootsRepository(session)

def tree_repo(session: AsyncSession = Depends(get_db_session)):
    return TreesRepository(session)

def soil_repo(session: AsyncSession = Depends(get_db_session)):
    return SoilsRepository(session)