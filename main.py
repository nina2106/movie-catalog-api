from fastapi import FastAPI
from config import settings

# Inicializamos la aplicación usando la configuración centralizada
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {"message": "Bienvenido al catálogo de películas"}