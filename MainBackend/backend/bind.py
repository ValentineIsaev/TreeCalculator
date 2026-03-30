import uvicorn
from app import app
from app.core import http_setting

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app.mount('/css', StaticFiles(directory="frontend/css"), )
app.mount('/imgs', StaticFiles(directory='frontend/imgs'))
app.mount('/scripts', StaticFiles(directory='frontend/scripts'))
# app.mount('/', StaticFiles(directory="frontend/html", html=True))

# @app.get('/index.h')
# def index():
#     return FileResponse('frontend/html/index.html')

@app.get('/')
def index():
    return FileResponse('frontend/html/index.html')

@app.get('/simulator')
def simulator():
    return FileResponse('frontend/html/simulator.html')

@app.get('/calculator')
def calculator():
    return FileResponse('frontend/html/calculator.html')

@app.get('/editor')
def editor():
    return FileResponse('frontend/html/editor.html')

@app.get('/set_soil')
def set_soil():
    return FileResponse('frontend/html/set_soil.html')

@app.get('/set_tree')
def set_tree():
    print('SET TREE')
    return FileResponse('frontend/html/set_tree.html')

if __name__ == '__main__':
    uvicorn.run(app,
                host=http_setting.SELF_URL,
                port=http_setting.SELF_PORT
)
