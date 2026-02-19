from fastapi import APIRouter, HTTPException
from database import MovieDatabase
from models import MovieCreate, MovieUpdate, MovieResponse, MovieListResponse

router = APIRouter(tags=["Movies"])
db = MovieDatabase()

# -------------------- CRUD Películas --------------------

@router.post("/movies", status_code=201, response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    data = movie.model_dump()
    created = db.add_movie(data)
    return {
        "success": True,
        "message": "Película creada correctamente 🎬",
        "data": created
    }

@router.get("/movies", response_model=MovieListResponse)
def list_movies():
    items = db.list_movies()
    return {
        "success": True,
        "message": f"Se encontraron {len(items)} películas 🍿",
        "data": items,
        "total": len(items)
    }

@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    movie = db.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    return {
        "success": True,
        "message": "Película encontrada correctamente 🎬",
        "data": movie
    }

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, changes: MovieUpdate):
    movie = db.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    update_data = changes.model_dump(exclude_unset=True)
    movie.update(update_data)
    db.movies[movie_id] = movie
    db.save_data()
    return {
        "success": True,
        "message": f"Película con ID {movie_id} actualizada correctamente 🎬",
        "data": movie
    }

@router.delete("/movies/{movie_id}", response_model=MovieResponse)
def delete_movie(movie_id: int):
    movie = db.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    del db.movies[movie_id]
    db.save_data()
    return {
        "success": True,
        "message": f"Película con ID {movie_id} eliminada correctamente 🗑️",
        "data": None
    }
