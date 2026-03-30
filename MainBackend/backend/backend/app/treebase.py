import requests
from typing import Optional, Any
from .calculate.tree import Tree

class TreeBaseHttp:
    def __init__(self, url: str):
        self._url = url

    def _create_request(self, url: str, **query) -> str:
        return self._url + url + '?' + '&'.join(f'{name}={value}' for name, value in query.items())

    def create_soil(self, soil_name: str, soil_c: float) -> int:
        response = requests.post(self._create_request('/create-soil'), json={
            'name': soil_name,
            'soil_c': soil_c
        })

        return response.status_code

    def get_tree(self, tree_id: int, soil_id: int) -> Tree:
        data = requests.get(self._create_request('/get-tree', tree_id=tree_id, soil_id=soil_id))
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
            max_strength=tree['max_stress']
        )

    def get_soil_c(self, soil_id: int) -> float:
        data = requests.get(self._create_request('/get-soil', soil_id=soil_id))
        return data.json()['soil_c']

    def get_soils(self, mod: str, tree_id: Optional[int]=None) -> dict[int, dict[str, Any]]:
        query = {}
        if mod == 'All':
            query['mod'] = 'All'
        elif mod == 'byTree':
            query['mod'] = 'byTree'
            query['tree_id'] = tree_id
        data = requests.get(self._create_request('/get-soils', **query))
        return data.json()

    def get_trees(self, mod: str, soil_id: Optional[int]=None) -> dict[int, dict[str, Any]]:
        query = {}
        if mod == 'All':
            query['mod'] = 'All'
        elif mod == 'bySoil':
            query['mod'] = 'bySoil'
            query['soil_id'] = soil_id
        elif mod == 'Old':
            query['mod'] = 'Old'
        data = requests.get(self._create_request('/get-trees', **query))
        return data.json()

    def create_root(self, tree_id: int, soil_id: int, a: float, b: float) -> int:
        response = requests.post(self._create_request('/create-root', soil_id=soil_id, tree_id=tree_id), json={
            'a': a,
            'b': b
        })

        return response.status_code

    def create_tree(self,
                    name: str,
                    height: float,
                    weight: float,
                    center_gravity_height: float,
                    diameter: float,
                    c_d: float,
                    square: float,
                    max_stress: float,
                    type_root: str,
                    info: str
                    ) -> int:
        response = requests.post(self._create_request('/create-tree'), json={
            'name': name,
            'height': height,
            'weight': weight,
            'center_gravity_height': center_gravity_height,
            'diameter': diameter,
            'c_d': c_d,
            'crown_square': square,
            'max_stress': max_stress,
            'type_root': type_root,
            'info': info
        })

        return response.status_code