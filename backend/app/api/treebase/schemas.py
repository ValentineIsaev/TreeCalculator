from pydantic import BaseModel

class CreateTreeBody(BaseModel):
    name: str
    height: float
    weight: float
    center_gravity_height: float
    diameter: float
    c_d: float
    square: float
    max_stress: float
    type_root: str
    # base_soil_id: int
    # a: float
    # b: float
    info: str

class CreateRoot(BaseModel):
    tree_id: int
    soil_id: int

    a: float
    b: float


class CreateSoilBody(BaseModel):
    name: str
    soil_c: float