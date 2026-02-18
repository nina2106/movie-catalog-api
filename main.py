from fastapi import FastAPI
from models import MovieCreate  # <- importamos el modelo de entrada

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