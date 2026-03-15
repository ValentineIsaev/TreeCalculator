from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from .models import Tree, Root, Soil, BaseModel

db_base = TypeVar('db_base')
class BaseRepository(Generic[db_base]):
    def __init__(self, session: AsyncSession, base: BaseModel):
        self._db = session
        self._base = base

    async def get_by_id(self, id_: int) -> db_base:
        stmt = select(self._base).where(self._base.id == id_)

        r = await self._db.execute(stmt)
        return r.scalar()


class TreesRepository(BaseRepository[Tree]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tree)
        self._db = session

    async def get_all(self) -> tuple[Tree, ...]:
        r = await self._db.execute(select(Tree))
        return tuple(r.scalars().all())

    async def create_tree(self, tree: Tree):
        self._db.add(tree)
        await self._db.commit()

    async def get_by_name(self, name: str) -> Tree:
        stmt = select(Tree).where(Tree.name == name)
        r = await self._db.execute(stmt)

        return r.scalar()

class SoilsRepository(BaseRepository[Soil]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Soil)
        self._db = session

    async def get_all(self) -> tuple[Soil, ...]:
        r = await self._db.execute(select(Soil))
        return tuple(r.scalars().all())

    async def get_by_name(self, name: str) -> Soil:
        stmt = select(Soil).where(Soil.name == name)
        r = await self._db.execute(stmt)
        return r.scalar()

    async def create_soil(self, soil: Soil):
        self._db.add(soil)
        await self._db.commit()

class RootsRepository(BaseRepository[Root]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Root)
        self._db = session

    async def get_root(self, tree_name: str, soil_type: str) -> Root:
        stmt = select(Root).where(and_(Root.name_tree == tree_name, Root.type_soil == soil_type))
        r = await self._db.execute(stmt)

        return r.scalar()

    async def create_root(self, root: Root):
        self._db.add(root)
        await self._db.commit()