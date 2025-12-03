from fastapi import status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


async def http_exception_handler(request, exc: HTTPException):
    """HTTP 예외 처리 핸들러"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Exception",
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )


async def general_exception_handler(request, exc: Exception):
    """일반 예외 처리 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "status_code": 500,
            "detail": "서버에서 오류가 발생했습니다. 나중에 다시 시도해주세요."
        }
    )
