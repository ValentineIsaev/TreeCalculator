from fastapi import FastAPI, Depends, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from treebase.postgres import (root_repo, tree_repo, soil_repo, Tree, Root, Soil,
                               TreesRepository, SoilsRepository, RootsRepository)
from .schemas import GetTreesBody, TreeDataBody, GetSoilDataBody, PostNewSoilDataBody, NewTypeTreeBody, NewTreeDataBody, ResponseSoilData
from MathTools import utils

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get('/get_trees')
async def get_trees(tree_database: TreesRepository = Depends(tree_repo)):
    trees = await tree_database.get_all()

    return {tree.id: GetTreesBody(name=tree.name,
                         height=tree.height,
                         weight=tree.weight,
                         diameter=tree.diameter,
                         crown_square=tree.crown_square,
                         type_root=tree.type_root,
                         info=tree.info) for tree in trees}

@app.get('/get_tree_data')
async def get_tree(tree_id: int = Query(),
                   soil_id: int = Query(),
                   tree_database: TreesRepository = Depends(tree_repo),
                   root_database: RootsRepository = Depends(root_repo),
                   soil_database: SoilsRepository = Depends(soil_repo)):
    tree = await tree_database.get_by_id(tree_id)
    soil = await soil_database.get_by_id(soil_id)
    root = await root_database.get_root(tree.name, soil.name)
    return TreeDataBody(
        name=tree.name,
        height=tree.height,
        weight=tree.weight,
        center_gravity_height=tree.center_gravity_height,
        diameter=tree.diameter,
        c_d=tree.c_d,
        crown_square=tree.crown_square,
        a=root.a,
        b=root.b,
        type_root=tree.type_root,
        info=tree.info
    )

@app.get('/get-soils')
async def get_soils(soil_database: SoilsRepository = Depends(soil_repo)):
    soils = await soil_database.get_all()
    return {soil.id: ResponseSoilData(name=soil.name,
                                      c=soil.soil_c) for soil in soils}

@app.get('/get_soil')
async def get_soil(soil_id: int = Query(),
                   soil_database: SoilsRepository = Depends(soil_repo)):
    soil = await soil_database.get_by_id(soil_id)
    return GetSoilDataBody(name=soil.name,
                           soil_c=soil.soil_c)

@app.post('/create_tree')
async def create_tree(tree: NewTreeDataBody,
                      tree_database: TreesRepository = Depends(tree_repo)):
    await tree_database.create_tree(Tree(
        name=tree.name,
        height=tree.height,
        weight=tree.weight,
        center_gravity_height=tree.center_gravity_height,
        diameter=tree.diameter,
        c_d=tree.c_d,
        crown_square=tree.crown_square,
        type_root=tree.type_root,
        info=tree.info
    ))

app.post('/create_new_tree_type')
async def create_new_tree_type(body: NewTypeTreeBody,
                               tree_id: int = Query(),
                               soil_id: int = Query(),
                               root_database: RootsRepository = Depends(root_repo),
                               tree_database: TreesRepository = Depends(tree_repo),
                               soil_database: SoilsRepository = Depends(soil_repo)):
    tree = await tree_database.get_by_id(tree_id)
    if not tree: raise HTTPException(status_code=404,
                                     detail=f'Wrong tree id: {tree_id}')

    soil = await soil_database.get_by_id(soil_id)
    if not soil: raise HTTPException(status_code=404,
                                     detail=f'Wrong soil id: {soil_id}')
    if not utils.tree_stability(body.a, body.b, soil.soil_c, tree.weight, tree.center_gravity_height, tree.height):
        raise HTTPException(status_code=404,
                            detail=f'Wrong a ({body.a}) and b ({body.b}) for tree {tree.name} in soil {soil.name}')

    await root_database.create_root(Root(
        name_tree=tree.name,
        type_soil=soil.name,
        a=body.a,
        b=body.b
    ))


@app.post('/create_soil')
async def create_soil(new_value: PostNewSoilDataBody,
                      soil_database: SoilsRepository = Depends(soil_repo)):
    await soil_database.create_soil(Soil(name=new_value.name,
                                         soil_c=new_value.soil_c))
