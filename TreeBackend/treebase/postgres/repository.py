from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update

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


    async def get_by_list_id(self, ids: tuple[int, ...]) -> tuple[db_base, ...]:
        stmt = select(self._base).where(self._base.id.in_(ids))
        result = await self._db.execute(stmt)

        return tuple(result.scalars().all())


class TreesRepository(BaseRepository[Tree]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tree)
        self._db = session

    async def get_old_trees(self) -> tuple[Tree, ...]:
        stmt = select(Tree).where(Tree.is_new == False)
        result = await self._db.execute(stmt)

        return tuple(result.scalars().all())

    async def get_all(self) -> tuple[Tree, ...]:
        r = await self._db.execute(select(Tree))
        return tuple(r.scalars().all())

    async def create_tree(self, tree: Tree):
        self._db.add(tree)
        # await self._db.commit()

    async def get_by_name(self, name: str) -> Tree:
        stmt = select(Tree).where(Tree.name == name)
        r = await self._db.execute(stmt)

        return r.scalar()

    async def set_is_not_new(self, tree_id: int) -> None:
        stmt = update(Tree).where(
            Tree.id == tree_id
        ).values(
            is_new=False
        )
        await self._db.execute(stmt)
        # await self._db.commit()


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
        # await self._db.commit()

class RootsRepository(BaseRepository[Root]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Root)
        self._db = session

    async def get_root(self, tree_id: int, soil_id: int) -> Root:
        stmt = select(Root).where(and_(Root.tree_id == tree_id, Root.soil_id == soil_id))
        r = await self._db.execute(stmt)

        return r.scalar()

    async def create_root(self, root: Root):
        self._db.add(root)
        # await self._db.commit()

    async def get_trees_by_soil(self, soil_id: int) -> tuple[int, ...]:
        stmt = select(Root.tree_id).where(Root.soil_id == soil_id)
        result = await self._db.execute(stmt)

        return tuple(result.scalars().all())

    async def get_soils_by_tree(self, tree_id: int) -> tuple[int, ...]:
        stmt = select(Root.soil_id).where(Root.tree_id == tree_id)
        result = await self._db.execute(stmt)

        return tuple(result.scalars().all())
