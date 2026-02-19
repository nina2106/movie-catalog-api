from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import date


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título de la película")
    director: str = Field(..., min_length=1, max_length=100, description="Director o directora")
    year: int = Field(..., ge=1880, le=2030, description="Año de estreno")
    genre: str = Field(..., min_length=1, max_length=50, description="Género principal")
    duration: Optional[int] = Field(None, ge=1, le=600, description="Duración en minutos")
    rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="Calificación (0–10)")
    description: Optional[str] = Field(None, max_length=1000, description="Breve descripción")
    price: Optional[float] = Field(None, ge=0.0, description="Precio de venta o renta")
    is_watched: bool = Field(default=False, description="Indica si la película ya fue vista")

    # Validaciones personalizadas
    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value < 1880:
            raise ValueError("El año debe ser >= 1880")
        if value > date.today().year + 5:
            raise ValueError("El año no puede estar más de 5 años en el futuro")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El título no puede estar vacío o solo con espacios")
        return value.strip()


class MovieCreate(MovieBase):
    """Modelo para crear una película"""
    class Config:
        schema_extra = {
            "example": {
                "title": "Avatar: The Way of Water",
                "director": "James Cameron",
                "year": 2022,
                "genre": "Sci-Fi",
                "duration": 192,
                "rating": 8.5,
                "description": "Secuela de Avatar que sigue la historia de Pandora y la familia de Jake Sully.",
                "price": 15.0,
                "is_watched": False
            }
        }


class MovieUpdate(BaseModel):
    """Modelo para actualizar parcialmente una película"""
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
    data: Optional[dict] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Película creada correctamente 🎬",
                "data": {
                    "id": 5,
                    "title": "Avatar: The Way of Water",
                    "director": "James Cameron",
                    "year": 2022,
                    "genre": "Sci-Fi",
                    "duration": 192,
                    "rating": 8.5,
                    "description": "Secuela de Avatar que sigue la historia de Pandora y la familia de Jake Sully.",
                    "price": 15.0,
                    "is_watched": False
                }
            }
        }


class MovieListResponse(BaseModel):
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje para el cliente")
    data: List[dict] = Field(default_factory=list, description="Listado de películas")
    total: int = Field(..., description="Cantidad total de elementos devueltos")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Se encontraron 4 películas 🍿",
                "data": [
                    {
                        "id": 1,
                        "title": "Interstellar",
                        "director": "Christopher Nolan",
                        "year": 2014,
                        "genre": "Sci-Fi",
                        "duration": 169,
                        "rating": 9.0,
                        "description": "Un grupo de exploradores viaja a través de un agujero de gusano en el espacio.",
                        "price": 12.5,
                        "is_watched": True
                    },
                    {
                        "id": 2,
                        "title": "Inception",
                        "director": "Christopher Nolan",
                        "year": 2010,
                        "genre": "Sci-Fi",
                        "duration": 148,
                        "rating": 9.5,
                        "description": "Un ladrón roba secretos a través de los sueños de las personas.",
                        "price": 10.0,
                        "is_watched": False
                    }
                ],
                "total": 4
            }
        }


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Siempre False en errores")
    message: str = Field(..., description="Mensaje breve para el cliente")
    error_code: Optional[str] = Field(None, description="Código interno opcional")
    details: Optional[dict] = Field(None, description="Metadatos del error (opcional)")
