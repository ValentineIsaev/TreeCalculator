from fastapi import Query, HTTPException

from ..calculate import CalculateManager, Simulator
from ..core import context, tree_base_http


def _check_client_id(client_id: int):
    if not context.is_client_exist(client_id): raise HTTPException(
        status_code=404,
        detail=f'Client with id {client_id} does not exist'
    )

def client_calculator(client_id: int = Query()):
    _check_client_id(client_id)
    calculator = context.get_calculate_manager(client_id)
    if calculator is None:
        calculator = CalculateManager()
        context.set_calculate_manager(client_id, calculator)
    return calculator

def client_simulator(client_id: int = Query()):
    _check_client_id(client_id)
    simulator = context.get_simulator(client_id)
    if simulator is None:
        simulator = Simulator()
        context.set_simulator(client_id, simulator)
    return simulator

def tree_base():
    return tree_base_http