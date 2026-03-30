from pydantic import BaseModel

class SetDataBody(BaseModel):
    tree_id: int
    soil_id: int

class ResponseStaticSimulationData(BaseModel):
    wind_speed_break: float
    wind_speed_tipping: float
    wind_speed_separation: float

    tipping_angle: float
    separation_angle: float

    root_moment: float
    resistance_moment: float

class ResponseSimulationData(BaseModel):
    roll_angle: float
    stress: float
    safety_factor: float
    wind_moment: float
    wind_force: float
    soil_moment: float
    weight_moment: float

    tree_status: str
