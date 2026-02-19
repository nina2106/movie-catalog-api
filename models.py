from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import date


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,description="Título de la película")
    director: str = Field(..., min_length=1, max_length=100,description="Director o directora")
    year: int = Field(..., ge=1880, le=2030, description="Año de estreno")
    genre: str = Field(..., min_length=1, max_length=50, description="Género principal")
    duration: Optional[int] = Field(None, ge=1, le=600, description="Duración en minutos")
    rating: Optional[float] = Field( None, ge=0.0, le=10.0, description="Calificación (0–10)")
    description: Optional[str] = Field(None, max_length=1000, description="Breve descripción")
    price: Optional[float] = Field( None, ge=0.0, description="Precio de venta o renta")
    is_watched: bool = Field(default=False, description="Indica si la película ya fue vista")

    # --- VALIDACIONES PERSONALIZADAS ---

    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        """Valida que el año esté dentro de un rango realista."""
        if value < 1880:
            raise ValueError("El año debe ser mayor o igual a 1880 (inicio del cine moderno).")
        if value > date.today().year + 5:
            raise ValueError("El año no puede ser más de 5 años en el futuro.")
        return value

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        """El título no puede estar vacío ni solo contener espacios."""
        if not value.strip():
            raise ValueError("El título no puede estar vacío o solo con espacios.")
        return value.strip()


class MovieCreate(MovieBase):
    """Modelo usado para crear una nueva película."""
    pass


class MovieUpdate(BaseModel):
    """Modelo usado para actualizar parcialmente una película existente."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1880, le=2030)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    duration: Optional[int] = Field(None, ge=1, le=600)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, ge=0.0)
    is_watched: Optional[bool] = None


class MovieResponse(BaseModel):
    success: bool = Field(...)
    message: str = Field(...)
    # Por ahora usamos dict porque aún no definimos el modelo "Movie" en este punto.
    # En una cápsula posterior cambiaremos a: Optional[Movie]
    data: Optional[dict] = Field(None)


class MovieListResponse(BaseModel):
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje para el cliente")
    data: List[dict] = Field(default_factory=list,description="Listado de películas (dict) en este paso")
    total: int = Field(..., description="Cantidad total de elementos devueltos")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Siempre False en errores")
    message: str = Field(..., description="Mensaje breve para el cliente")
    error_code: Optional[str] = Field(None, description="Código interno opcional")
    details: Optional[dict] = Field(None, description="Metadatos del error (opcional)")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Siempre False en errores")
    message: str = Field(..., description="Mensaje breve para el cliente")
    error_code: Optional[str] = Field(None, description="Código interno opcional")
    details: Optional[dict] = Field(None, description="Metadatos del error (opcional)")    