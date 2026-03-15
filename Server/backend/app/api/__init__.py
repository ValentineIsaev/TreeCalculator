from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .simulator import simulator_router
from .common import app as common_router
from .calculator import calculate_router

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(simulator_router)
app.include_router(common_router)
app.include_router(calculate_router)