from fastapi import Depends, APIRouter
from fastapi.params import Query

from typing import Any

from backend.app.calculate import Simulator
from ...treebase import TreeBaseHttp
from ..DI import client_simulator, tree_base

from .schemas import *

app = APIRouter()

@app.post('/simulator/set-data')
async def set_data(data: SetDataBody,
                   simulator: Simulator=Depends(client_simulator),
                   tree_http= Depends(tree_base)):
    tree = tree_http.get_tree(data.tree_id, data.soil_id)
    soil_c = tree_http.get_soil_c(data.soil_id)
    static_data = simulator.set_data(tree, soil_c)
    return ResponseStaticSimulationData(
        wind_speed_break=static_data.wind_speed_break,
        wind_speed_tipping=static_data.wind_speed_tipping,
        wind_speed_separation=static_data.wind_speed_separation,
        tipping_angle=static_data.tipping_angle,
        separation_angle=static_data.separation_angle,
        root_moment=static_data.root_moment,
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
                                  soil_moment = data.soil_moment,
                                  weight_moment=data.weight_moment,
                                  tree_status=data.tree_status.value)

@app.get('/simulator/get-trees-by-soil')
def get_trees_by_soil(soil_id: int = Query(),
                      treebase: TreeBaseHttp = Depends(tree_base)) -> dict[int, dict[str, Any]]:
    data = treebase.get_trees('bySoil', soil_id=soil_id)
    return data

@app.get('/simulator/get-trees')
def get_trees(treebase: TreeBaseHttp = Depends(tree_base)) -> dict[int, dict[str, Any]]:
    data = treebase.get_trees('All')
    return data

@app.get('/simulator/get-soils-by-tree')
def get_soils_by_tree(tree_id: int = Query(),
                    treebase: TreeBaseHttp = Depends(tree_base)) -> dict[int, dict[str, Any]]:
    return treebase.get_soils('byTree', tree_id)

@app.get('/simulator/get-soils')
def get_soils(treebase: TreeBaseHttp = Depends(tree_base)) -> dict[int, dict[str, Any]]:
    return treebase.get_soils('All')