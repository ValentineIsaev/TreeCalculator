from fastapi import FastAPI, Depends, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from treebase.postgres import (root_repo, tree_repo, soil_repo, Tree, Root, Soil,
                               TreesRepository, SoilsRepository, RootsRepository)
from .schemas import GetTreesBody, TreeDataBody, GetSoilDataBody, PostNewSoilDataBody, NewRootBody, NewTreeDataBody, ResponseSoilData
from MathTools import math_tools

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get('/get-trees')
async def get_trees(mod: str = Query(),
                    soil_id: int = Query(None),
                    tree_database: TreesRepository = Depends(tree_repo),
                    root_database: RootsRepository = Depends(root_repo)):
    if mod == 'All':
        trees = await tree_database.get_all()

    elif mod == 'Old':
        trees = await tree_database.get_old_trees()

    elif mod == 'bySoil':
        if soil_id is None: raise HTTPException(status_code=404,
                                                detail='Soil id is None')
        tree_ids_by_soul = await root_database.get_trees_by_soil(soil_id)
        print('Tree ids by soil:', tree_ids_by_soul)
        tree_old = await tree_database.get_old_trees()
        print('Tree old', tree_old)
        tree_ids = tuple(set(set(tree_ids_by_soul) & set((tree.id for tree in tree_old))))

        trees = await tree_database.get_by_list_id(tree_ids)
    else:
        raise HTTPException(status_code=404,
                            detail=f'Wrong mod {mod}')


    return {tree.id: GetTreesBody(name=tree.name,
                                  height=tree.height,
                                  weight=tree.weight,
                                  diameter=tree.diameter,
                                  crown_square=tree.crown_square,
                                  type_root=tree.type_root,
                                  info=tree.info) for tree in trees}

@app.get('/get-tree')
async def get_tree(tree_id: int = Query(),
                   soil_id: int = Query(),
                   tree_database: TreesRepository = Depends(tree_repo),
                   root_database: RootsRepository = Depends(root_repo),
                   soil_database: SoilsRepository = Depends(soil_repo)):
    tree = await tree_database.get_by_id(tree_id)
    soil = await soil_database.get_by_id(soil_id)
    root = await root_database.get_root(tree_id, soil_id)
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
        max_stress=tree.max_stress,
        info=tree.info
    )

@app.get('/get-soils')
async def get_soils(mod: str = Query(),
                    tree_id: int = Query(None),
                    soil_database: SoilsRepository = Depends(soil_repo),
                    root_database: RootsRepository = Depends(root_repo)):
    if mod == 'All':
        soils = await soil_database.get_all()
    elif mod == 'byTree':
        if tree_id is None: raise HTTPException(status_code=404,
                                                detail='Tree id is None!')
        soils_ids = await root_database.get_soils_by_tree(tree_id)
        soils = await soil_database.get_by_list_id(soils_ids)
    else:
        raise HTTPException(status_code=404,
                            detail=f'Wrong mod {mod}')
    return {soil.id: ResponseSoilData(name=soil.name,
                                      c=soil.soil_c) for soil in soils}

@app.get('/get-soil')
async def get_soil(soil_id: int = Query(),
                   soil_database: SoilsRepository = Depends(soil_repo)):
    soil = await soil_database.get_by_id(soil_id)
    return GetSoilDataBody(name=soil.name,
                           soil_c=soil.soil_c)

@app.post('/create-tree')
async def create_tree(tree: NewTreeDataBody,
                      tree_database: TreesRepository = Depends(tree_repo)):
    if await tree_database.get_by_name(tree.name) is not None:
        raise HTTPException(status_code=402)
    await tree_database.create_tree(Tree(
        name=tree.name,
        height=tree.height,
        weight=tree.weight,
        center_gravity_height=tree.center_gravity_height,
        diameter=tree.diameter,
        c_d=tree.c_d,
        crown_square=tree.crown_square,
        max_stress=tree.max_stress,
        type_root=tree.type_root,
        info=tree.info,
        is_new=True
    ))


@app.post('/create-root')
async def create_root(body: NewRootBody,
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

    if not math_tools.tree_is_stability(body.a, body.b, soil.soil_c, tree.weight, tree.center_gravity_height):
        raise HTTPException(status_code=401,
                            detail=f'Wrong a ({body.a}) and b ({body.b}) for tree {tree.name} in soil {soil.name}')

    if await root_database.get_root(tree.id, soil.id) is not None:
        raise HTTPException(status_code=402,
                            detail='Root exist!')

    await root_database.create_root(Root(
        tree_id=tree_id,
        soil_id=soil_id,
        a=body.a,
        b=body.b
    ))
    if tree.is_new:
    #     print('SET')
        await tree_database.set_is_not_new(tree.id)


@app.post('/create-soil')
async def create_soil(new_value: PostNewSoilDataBody,
                      soil_database: SoilsRepository = Depends(soil_repo)):
    if await soil_database.get_by_name(new_value.name) is not None: raise HTTPException(status_code=402)
    await soil_database.create_soil(Soil(name=new_value.name,
                                         soil_c=new_value.soil_c))
