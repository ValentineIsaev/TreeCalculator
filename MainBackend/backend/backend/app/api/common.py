from ..core import context
from fastapi import APIRouter

app = APIRouter()

@app.get('/create_client')
def create_client():
    client_id = context.create_client()
    return {'id': client_id}