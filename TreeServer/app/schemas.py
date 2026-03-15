from pydantic import BaseModel
from typing import Optional

class NewTypeTreeBody(BaseModel):
    a: float
    b: float

class NewTreeDataBody(BaseModel):
    name: str

    height: float
    weight: float
    center_gravity_height: float
    diameter: float

    c_d: float
    crown_square: float

    type_root: str
    info: str

class TreeDataBody(BaseModel):
    name: str

    height: float
    weight: float
    center_gravity_height: float
    diameter: float

    c_d: float
    crown_square: float

    a: float
    b: float

    type_root: str
    info: str

    max_strength: Optional[float] = 0

class ResponseSoilData(BaseModel):
    name: str
    c: float

class GetTreesBody(BaseModel):
    name: str
    height: float
    weight: float
    diameter: float
    crown_square: float

    type_root: str
    info: str

class GetSoilDataBody(BaseModel):
    name: str
    soil_c: float


class PostNewSoilDataBody(BaseModel):
    name: str
    soil_c: float