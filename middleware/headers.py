from starlette.responses import JSONResponse

from serializers import HeadersStatus
from settings import settings

from fastapi import Request

async def check_headers(request: Request, call_next):
    auth_header = request.headers.get('Authorization')

    if auth_header != settings.token.AUTH_TOKEN.get_secret_value():
        return JSONResponse(
            status_code=401,
            content={
                "message": HeadersStatus.UNKNOWN_HEADER
            }
        )

    return await call_next(request)
