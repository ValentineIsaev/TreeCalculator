from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    pass

class Tree(BaseModel):
    __tablename__ = 'trees'

    name: Mapped[str]

    height: Mapped[float]
    weight: Mapped[float]
    center_gravity_height: Mapped[float]
    diameter: Mapped[float]

    c_d: Mapped[float]
    crown_square: Mapped[float]

    max_stress: Mapped[float]

    type_root: Mapped[str]

    info: Mapped[str]

    is_new: Mapped[bool] = mapped_column(default=True)


class Soil(BaseModel):
    __tablename__ = 'soils'

    name: Mapped[str]
    soil_c: Mapped[float]


class Root(BaseModel):
    __tablename__ = 'roots'

    tree_id: Mapped[int]
    soil_id: Mapped[int]

    a: Mapped[float]
    b: Mapped[float]
