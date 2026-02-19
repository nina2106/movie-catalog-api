from fastapi import FastAPI
import movies
from exceptions import register_exception_handlers



app = FastAPI(title="🎬 Movie Catalog API",
    description="")
''
# Registrar handlers centralizados
register_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo de películas"}

app.include_router(movies.router, prefix="/api/v1")

