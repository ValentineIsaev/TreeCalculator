from fastapi import Depends, APIRouter
from fastapi.params import Query

from backend.app.calculate import Simulator
from ..DI import client_simulator
from ...core import tree_base_http

from .schemas import *

app = APIRouter()

@app.post('/simulator/set-data')
async def set_data(data: SetDataBody,
                   simulator: Simulator=Depends(client_simulator),
                   tree_http=tree_base_http):
    tree = tree_http.get_tree(data.tree_id, data.soil_id)
    soil_c = tree_http.get_soil_c(data.soil_id)

    static_data = simulator.set_data(tree, soil_c)
    print(static_data)
    return ResponseStaticSimulationData(
        wind_speed_break=static_data.wind_speed_break,
        wind_speed_tipping=static_data.wind_speed_tipping,
        wind_speed_separation=static_data.wind_speed_separation,
        tipping_angle=static_data.tipping_angle,
        separation_angle=static_data.separation_angle,
        soil_moment=static_data.soil_moment,
        resistance_moment=static_data.resistance_moment
    )

@app.post('/simulator/run')
def start_simulation(simulator: Simulator=Depends(client_simulator)):
    simulator.run()

@app.post('/simulator/pause')
def pause_simulation(simulator: Simulator=Depends(client_simulator)):
    simulator.pause()

@app.post('/simulator/stop')
def stop_simulation(simulator: Simulator=Depends(client_simulator)):
    simulator.stop()

@app.post('/simulator/set-speed')
def set_wind_speed(speed: int = Query(),
                   simulator: Simulator=Depends(client_simulator)):
    simulator.set_wind_speed(speed)

@app.get('/simulator/simulation-data')
def get_simulation_data(simulator: Simulator=Depends(client_simulator)):
    data = simulator.get_simulate()

    return ResponseSimulationData(roll_angle=data.roll_angle,
                                  stress=data.stress,
                                  safety_factor=data.safety_factor,
                                  wind_moment=data.wind_moment,
                                  wind_force=data.wind_force,
                                  tree_status=data.tree_status.value)