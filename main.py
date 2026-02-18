from fastapi import FastAPI
from models import MovieCreate
import movies  # <--- Importamos nuestro nuevo módulo de rutas

app = FastAPI(title="Movie Catalog API")

@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo de películas"}

@app.post("/movies")
def create_movie(payload: MovieCreate):
    return {
        "success": True,
        "message": "Película creada correctamente",
        "data": payload.model_dump()
    }
    

# <--- Montamos las rutas del router en /api/v1
app.include_router(movies.router, prefix="/api/v1")