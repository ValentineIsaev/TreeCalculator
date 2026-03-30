from fastapi import APIRouter, Depends, HTTPException

from ..DI import tree_base
from ...treebase import TreeBaseHttp

from .schemas import *

app = APIRouter()

@app.get('/treebase/get-soils')
def get_soils(tree_http: TreeBaseHttp = Depends(tree_base)):
    return tree_http.get_soils(mod='All')

@app.get('/treebase/get-trees')
def get_trees(tree_http: TreeBaseHttp = Depends(tree_base)):
    return tree_http.get_trees(mod='All')

@app.post('/treebase/create-tree')
def create_tree(data: CreateTreeBody,
                tree_http: TreeBaseHttp = Depends(tree_base)):
    status = tree_http.create_tree(
        data.name,
        data.height,
        data.weight,
        data.center_gravity_height,
        data.diameter,
        data.c_d,
        data.square,
        data.max_stress,
        data.type_root,
        # data.base_soil_id,
        # data.a,
        # data.b,
        data.info
    )

    if status == 401:
        raise HTTPException(status_code=401)
    elif status == 402:
        raise HTTPException(status_code=402)

@app.post('/treebase/create-root')
def create_root(data: CreateRoot,
                tree_http: TreeBaseHttp = Depends(tree_base)):
    status = tree_http.create_root(data.tree_id, data.soil_id, data.a, data.b)
    if status == 401:
        raise HTTPException(status_code=401)
    elif status == 402:
        raise HTTPException(status_code=402)

@app.post('/treebase/create-soil')
def create_root(data: CreateSoilBody,
                treebase_http: TreeBaseHttp = Depends(tree_base)):
    status = treebase_http.create_soil(data.name, data.soil_c)
    if status == 402:
        raise HTTPException(status_code=402)