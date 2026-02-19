from fastapi import FastAPI
from models import MovieCreate
import movies

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import ErrorResponse

app = FastAPI(title="Movie Catalog API")


@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo de películas"}


@app.post("/movies")
def create_movie(payload: MovieCreate):
    return {
        "success": True,
        "message": "Película recibida (aún sin guardar)",
        "data": payload.model_dump()
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Estándar para errores que tú lanzas con HTTPException (ej. 404).
    """
    payload = ErrorResponse(
        success=False,
        message=str(exc.detail) if exc.detail else "HTTP error",
        error_code="HTTP_ERROR",
        details=None,
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Estándar para errores de validación 422 (Pydantic/FastAPI).
    Incluimos los 'errors()' en details para identificar campos con fallo.
    """
    payload = ErrorResponse(
        success=False,
        message="Validation error",
        error_code="VALIDATION_ERROR",
        details={"errors": exc.errors()},
    ).model_dump()
    return JSONResponse(status_code=422, content=payload)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catch-all para errores no controlados → 500.
    """
    payload = ErrorResponse(
        success=False,
        message="Internal server error",
        error_code="INTERNAL_ERROR",
        details=None,
    ).model_dump()
    return JSONResponse(status_code=500, content=payload)


app.include_router(movies.router, prefix="/api/v1")