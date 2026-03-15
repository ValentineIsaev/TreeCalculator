from fastapi import APIRouter
from ..DI import client_simulator, client_calculator
from fastapi import Query, HTTPException, Depends
from .calculate_schemas import *
from ...calculate import CalculateManager

app = APIRouter()

@app.post('/calculator/wind-load')
def calculate_wind_load(data: CalculateWindLoadBody,
                        calculator = Depends(client_calculator)):
    f, m = calculator.calculate_wind_load(data.wind_speed, data.c_d, data.crown_square, data.tree_height)

    return ResponseWindLoad(wind_force=f, wind_moment=m)

@app.post('/calculator/mechanical-strength')
def calculate_mechanical_strength(data: CalculateMechanicalStrengthBody,
                                  calculator: CalculateManager = Depends(client_calculator)):
    strength, safety = calculator.calculate_mechanical_strength(data.wind_speed,
                                                                data.c_d,
                                                                data.crown_square,
                                                                data.diameter,
                                                                data.max_strength)

    return ResponseMechanicalStrength(mechanical_strength=strength,
                                      safety=safety)

@app.post('/calculator/break-wind-speed')
def calculate_max_wind_speed_break(data: CalculateBreakWindSpeedBody,
                                   calculator: CalculateManager = Depends(client_calculator)):
    speed = calculator.calculate_max_wind_speed_break(data.diameter,
                                                      data.c_d,
                                                      data.crown_square,
                                                      data.tree_height,
                                                      data.max_strength)

    return ResponseBreakWindSpeed(wind_speed=speed)

@app.post('/calculator/roll-angle')
def calculate_roll_angle(data: CalculateRollAngleBody,
                         calculator: CalculateManager=Depends(client_calculator)):
    angle = calculator.calculate_roll_angle(data.wind_speed,
                                            data.soil_c,
                                            data.c_d,
                                            data.a,
                                            data.b,
                                            data.crown_square,
                                            data.tree_weight,
                                            data.center_gravity_height,
                                            data.tree_height)

    return ResponseRollAngle(angle=angle)

@app.post('/calculator/separation-angle')
def calculate_separation_angle(data: CalculateSeparationAngleBody,
                               calculator: CalculateManager = Depends(client_calculator)):
    angle = calculator.calculate_separation_angle(data.soil_c,
                                                  data.tree_weight,
                                                  data.a,
                                                  data.b)

    return ResponseSeparationAngle(angle=angle)

@app.post('/calculator/tipping-angle')
def calculate_tipping_angle(data: CalculateTippingAngleBody,
                            calculator: CalculateManager = Depends(client_calculator)):
    angle = calculator.calculate_tipping_angle(data.soil_c,
                                               data.tree_weight,
                                               data.center_gravity_height,
                                               data.b)

    return ResponseTippingAngle(angle=angle)

@app.post('/calculator/tipping-wind-speed')
def calculate_tipping_wind_speed(data: CalculateWindTippingBody,
                                 calculator: CalculateManager = Depends(client_calculator)):
    speed = calculator.calculate_max_wind_tipping(data.soil_c,
                                                  data.tree_weight,
                                                  data.center_gravity_height,
                                                  data.a,
                                                  data.b,
                                                  data.c_d,
                                                  data.crown_square,
                                                  data.tree_weight)

    return ResponseWindTipping(wind_speed=speed)

@app.post('/calculator/separation-wind-speed')
def calculate_separation_wind_speed(data: CalculateSeparationWindSpeedBody,
                                    calculator: CalculateManager = Depends(client_calculator)):
    speed = calculator.calculate_separation_wind_speed(data.tree_weight,
                                                       data.soil_c,
                                                       data.a,
                                                       data.b,
                                                       data.center_gravity_height,
                                                       data.tree_height,
                                                       data.c_d,
                                                       data.crown_square)

    return ResponseSeparationWindSpeed(wind_speed=speed)