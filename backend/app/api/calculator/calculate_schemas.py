from pydantic import BaseModel

class CalculateWindLoadBody(BaseModel):
    wind_speed: float
    c_d: float
    crown_square: float
    tree_height: float

class ResponseWindLoad(BaseModel):
    wind_force: float
    wind_moment: float

class CalculateMechanicalStrengthBody(BaseModel):
    wind_speed: float
    c_d: float
    crown_square: float
    diameter: float
    max_strength: float

class ResponseMechanicalStrength(BaseModel):
    mechanical_strength: float
    safety: float

class CalculateBreakWindSpeedBody(BaseModel):
    diameter: float
    c_d: float
    crown_square: float
    tree_height: float
    max_strength: float


class ResponseBreakWindSpeed(BaseModel):
    wind_speed: float

class CalculateRollAngleBody(BaseModel):
    wind_speed: float
    soil_c: float
    c_d: float
    a: float
    b: float
    crown_square: float
    tree_weight: float
    center_gravity_height: float
    tree_height: float

class ResponseRollAngle(BaseModel):
    angle: float

class CalculateSeparationAngleBody(BaseModel):
    soil_c: float
    tree_weight: float
    a: float
    b: float

class ResponseSeparationAngle(BaseModel):
    angle: float

class CalculateTippingAngleBody(BaseModel):
    soil_c: float
    tree_weight: float
    center_gravity_height: float
    b: float

class ResponseTippingAngle(BaseModel):
    angle: float

class CalculateWindTippingBody(BaseModel):
    soil_c: float
    tree_weight: float
    center_gravity_height: float
    a: float
    b: float
    c_d: float
    crown_square: float
    tree_height: float

class ResponseWindTipping(BaseModel):
    wind_speed: float

class CalculateSeparationWindSpeedBody(BaseModel):
    tree_weight: float
    soil_c: float
    a: float
    b: float
    center_gravity_height: float
    tree_height: float
    c_d: float
    crown_square: float

class ResponseSeparationWindSpeed(BaseModel):
    wind_speed: float
