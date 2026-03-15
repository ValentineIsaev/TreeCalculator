import requests
from .calculate.tree import Tree

class TreeBaseHttp:
    def __init__(self, url: str):
        self._url = url

    def _create_request(self, url: str, **query) -> str:
        return self._url + url + '?' + '&'.join(f'{name}={value}' for name, value in query.items())

    def get_tree(self, tree_id: int, soil_id: int) -> Tree:
        data = requests.get(self._create_request('/get_tree_data', tree_id=tree_id, soil_id=soil_id))
        tree = data.json()
        return Tree(
            tree_height=tree['height'],
            tree_weight=tree['weight'],
            center_gravity_height=tree['center_gravity_height'],
            diameter=tree['diameter'],
            c_d=tree['c_d'],
            crown_square=tree['crown_square'],
            a=tree['a'],
            b=tree['b'],
            max_strength=tree['max_strength']
        )

    def get_soil_c(self, soil_id: int) -> float:
        data = requests.get(self._create_request('/get_soil', soil_id=soil_id))
        return data.json()['soil_c']