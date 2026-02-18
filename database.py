from pathlib import Path
import json
from typing import Dict, List, Optional

DEFAULT_DB_FILE = "movies.json"

DB_PATH: Path = Path(__file__).with_name(DEFAULT_DB_FILE)


def get_db_path() -> Path:
    return DB_PATH


def ensure_db_file_exists() -> Path:
    """
    Crea el archivo movies.json si no existe.
    No escribe datos todavía, solo garantiza que el archivo esté presente.
    """
    path = get_db_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    return path


class MovieDatabase:
    """
    Clase que actúa como base de datos en memoria para el catálogo de películas.
    Por ahora, solo mantiene los datos temporalmente mientras la app está activa.
    """

    def __init__(self, file_path: Optional[str] = None):
        self.movies: Dict[int, Dict] = {}
        self.next_id: int = 1

        self._file_path: Path = Path(file_path) if file_path else get_db_path()
        ensure_db_file_exists()
        self.load_data()

    # ---------------------------------------------------------------------
    # Persistencia
    # ---------------------------------------------------------------------
    def load_data(self) -> None:
        try:
            text = self._file_path.read_text(encoding="utf-8").strip()
            if not text:
                self.movies = {}
                self.next_id = 1
                self.save_data()
                return

            data = json.loads(text)

            movies_list: List[Dict] = data.get("movies", [])
            next_id_val: int = data.get("next_id", 1)

            self.movies = {}
            for item in movies_list:
                movie_id = item.get("id")
                if isinstance(movie_id, int):
                    self.movies[movie_id] = item

            if isinstance(next_id_val, int) and next_id_val > 0:
                self.next_id = next_id_val
            else:
                self.next_id = (max(self.movies.keys()) +
                                1) if self.movies else 1

        except Exception as e:
            print(f"[MovieDatabase.load_data] Error al cargar datos: {e}")
            self.movies = {}
            self.next_id = 1
            self.save_data()

    def save_data(self) -> None:
        try:
            data = {
                "movies": list(self.movies.values()),
                "next_id": self.next_id
            }
            self._file_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[MovieDatabase.save_data] Error al guardar datos: {e}")

    # ---------------------------------------------------------------------
    # Operaciones en memoria
    # ---------------------------------------------------------------------

    def add_movie(self, movie_data: dict) -> dict:
        """
        Agrega una nueva película al catálogo.
        Aún no guarda en JSON (solo memoria).
        """
        movie_id = self.next_id
        self.movies[movie_id] = {"id": movie_id, **movie_data}
        self.next_id += 1
        self.save_data()
        return self.movies[movie_id]

    def list_movies(self) -> list[dict]:
        """Devuelve todas las películas actualmente en memoria."""
        return list(self.movies.values())

    def get_movie(self, movie_id: int) -> dict | None:
        """Devuelve una película específica por ID (o None si no existe)."""
        return self.movies.get(movie_id)