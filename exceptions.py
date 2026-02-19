from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import ErrorResponse
import logging

# Configuramos un logger básico
logger = logging.getLogger("uvicorn.error")


def register_exception_handlers(app):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        payload = ErrorResponse(
            success=False,
            message=str(exc.detail),
            error_code="HTTP_ERROR",
            details={"path": request.url.path},
        ).model_dump(exclude_none=True)  # elimina campos None
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Mapeamos errores de Pydantic a un formato más limpio
        errors = [
            {"loc": e["loc"], "msg": e["msg"], "type": e["type"]}
            for e in exc.errors()
        ]
        payload = ErrorResponse(
            success=False,
            message="Validation error",
            error_code="VALIDATION_ERROR",
            details={"path": request.url.path, "errors": errors},
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Logueamos el error completo para debug en producción
        logger.error(f"Unhandled error at {request.url.path}: {exc}", exc_info=True)

        payload = ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            details={"path": request.url.path},
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=500, content=payload)
