from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ErrorResponse
from exceptions import register_exception_handlers
from movies import router as movies_router

app = FastAPI(
    title="🎬 Movie Catalog API",
    description="API bienvenidos al catalogo de peliculas",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar handlers personalizados
register_exception_handlers(app)

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo de películas 🍿"}

# Registrar rutas de películas
app.include_router(movies_router, prefix="/api/v1")
