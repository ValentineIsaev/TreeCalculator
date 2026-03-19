from .env_configs import HttpSettings

from .context import ClientContext

from .treebase import TreeBaseHttp

context = ClientContext()
# app = FastAPI()
# app.add_middleware(ClientSessionMiddleware, context=context)

http_setting = HttpSettings()
tree_base_http = TreeBaseHttp(http_setting.TREE_BASE_HTTP_URL)
