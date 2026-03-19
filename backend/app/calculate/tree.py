from pydantic import BaseModel
from enum import Enum

class TreeAttrs(Enum):
    TREE_HEIGHT = 'tree_height'
    TREE_WEIGHT = 'ree_weight'
    CENTER_GRAVITY_HEIGHT = 'center_gravity_height'
    MAX_STRENGTH = 'max_strength'
    DIAMETER = 'diameter'
    C_D = 'c_d'

    CROWN_SQUARE = 'crown_square'

    A = 'a'
    B = 'b'

class Tree(BaseModel):
    tree_height: float
    tree_weight: float
    center_gravity_height: float
    max_strength: float
    diameter: float
    c_d: float

    crown_square: float

    a: float
    b: float

    def get_attrs(self, *attrs: TreeAttrs) -> tuple:
        return tuple([getattr(self, attr.value) for attr in attrs])
