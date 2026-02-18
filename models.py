from typing import Optional
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    # Título de la película. Obligatorio.
    title: str = Field(..., min_length=1, max_length=200,
                       description="Título de la película")

    # Director. Obligatorio, texto corto.
    director: str = Field(..., min_length=1, max_length=100,
                          description="Director o directora")

    # Año de estreno. Debe estar dentro de un rango realista.
    year: int = Field(..., ge=1880, le=2030, description="Año de estreno")

    # Género principal. Ejemplo: Acción, Drama, Sci-Fi, etc.
    genre: str = Field(..., min_length=1, max_length=50,
                       description="Género principal")

    # Duración en minutos. Puede omitirse.
    duration: Optional[int] = Field(
        None, ge=1, le=600, description="Duración en minutos")

    # Calificación promedio (de 0 a 10). Puede omitirse.
    rating: Optional[float] = Field(
        None, ge=0.0, le=10.0, description="Calificación promedio")

    # Breve descripción de la película.
    description: Optional[str] = Field(
        None, max_length=1000, description="Descripción breve")

    # Precio (opcional). Si existe, debe ser mayor o igual a 0.
    price: Optional[float] = Field(
        None, ge=0.0, description="Precio de venta o renta")

    # Indica si la película ya fue vista.
    is_watched: bool = Field(
        default=False, description="Indica si la película ya fue vista")


class MovieCreate(MovieBase):
    """Modelo usado para crear una nueva película (POST)."""
    pass