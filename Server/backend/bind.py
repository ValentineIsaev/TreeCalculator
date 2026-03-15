import uvicorn
from app import app
from app.core import http_setting

if __name__ == '__main__':
    uvicorn.run(app,
                host=http_setting.SELF_URL,
                port=http_setting.SELF_PORT)
