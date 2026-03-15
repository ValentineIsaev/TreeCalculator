from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    pass

class Tree(BaseModel):
    __tablename__ = 'Trees'

    name: Mapped[str]

    height: Mapped[float]
    weight: Mapped[float]
    center_gravity_height: Mapped[float]
    diameter: Mapped[float]

    c_d: Mapped[float]
    crown_square: Mapped[float]

    type_root: Mapped[Optional[str]] = mapped_column()

    info: Mapped[str]


class Soil(BaseModel):
    __tablename__ = 'Soils'

    name: Mapped[str]
    soil_c: Mapped[float]


class Root(BaseModel):
    __tablename__ = 'Roots'

    name_tree: Mapped[str]
    type_soil: Mapped[str]

    a: Mapped[Optional[int]]
    b: Mapped[Optional[int]]
