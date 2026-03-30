from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from fastapi.responses import JSONResponse

from ..context import ClientContext
from ..calculate import CalculateManager, Simulator

class ClientSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, context: ClientContext):
        super().__init__(app)
        self._context = context

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_id = request.query_params.get('client_id')
        if not client_id is None:
            try:
                client_id = int(client_id)
                if not self._context.is_client_exist(client_id):
                    raise ValueError(f'Client with id {client_id} not exist')

                if self._context.get_simulator(client_id) is None:
                    self._context.set_simulator(simulator=Simulator())
                if self._context.get_calculate_manager(client_id) is None:
                    self._context.set_calculate_manager(CalculateManager())
            except ValueError as e:
                if str(e).startswith('invalid literal for int()'):
                    return JSONResponse(
                        status_code=404,
                        content={'detail': f'Wrong value for client id: {client_id}'}
                    )
                if str(e).startswith('Client with id'):
                    return JSONResponse(
                        status_code=404,
                        content={'detail': str(e)}
                    )

        return await call_next(request)
