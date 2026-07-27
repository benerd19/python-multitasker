from .exceptions import AppException
from fastapi.responses import JSONResponse
from fastapi import Request

async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "detail": exc.detail
            } 
        }
    )