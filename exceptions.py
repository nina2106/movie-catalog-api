from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import ErrorResponse

def register_exception_handlers(app):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        payload = ErrorResponse(
            success=False,
            message=str(exc.detail),
            error_code="HTTP_ERROR",
            details=None,
        ).model_dump()
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        payload = ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"errors": exc.errors()},
        ).model_dump()
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        payload = ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            details=None,
        ).model_dump()
        return JSONResponse(status_code=500, content=payload)
