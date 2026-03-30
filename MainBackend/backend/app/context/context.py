from typing import Optional
from ..calculate import CalculateManager, Simulator


def check_client_id(method):
    def wrapper(self, client_id: int, *args, **kwargs):
        if client_id not in self._data.keys(): raise ValueError(f'Wrong client id: {client_id}')
        return method(self, client_id, *args, **kwargs)
    return wrapper

class ClientContext:
    _CALCULATE_NAME = 'calculator'
    _SIMULATOR_NAME = 'simulator'

    def __init__(self):
        self._data = {}

    @check_client_id
    def get_calculate_manager(self, client_id: int) -> Optional[CalculateManager]:
        return self._data.get(client_id).get(self._CALCULATE_NAME)

    @check_client_id
    def get_simulator(self, client_id: int) -> Optional[Simulator]:
        return self._data.get(client_id).get(self._SIMULATOR_NAME)

    @check_client_id
    def set_simulator(self, client_id: int, simulator: Simulator) -> None:
        self._data[client_id][self._SIMULATOR_NAME] = simulator

    @check_client_id
    def set_calculate_manager(self, client_id: int, calculate_manager: CalculateManager) -> None:
        self._data[client_id][self._CALCULATE_NAME] = calculate_manager

    @check_client_id
    def reset_client_data(self, client_id: int) -> None:
        del self._data[client_id]

    def is_client_exist(self, client_id: int) -> bool:
        print(id(self))
        print(client_id, list(self._data.keys()))
        print(self._data.get(client_id))
        return self._data.get(client_id) is not None

    def create_client(self) -> int:
        """
        Создает клиента в контексте
        :return: уникальный id клиента
        """

        new_client_id = max(self._data.keys())+1 if self._data.keys() else 0
        self._data[new_client_id] = {
            self._SIMULATOR_NAME: None,
            self._CALCULATE_NAME: None
        }
        return new_client_id