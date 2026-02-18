try:
    from fastapi import FastAPI
    app = FastAPI(title="Movie Catalog API")
except Exception:
    # Permite que el archivo exista antes de instalar FastAPI
    app = None