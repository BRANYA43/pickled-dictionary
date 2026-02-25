from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent

DATABASE_FILE: Path = BASE_DIR / 'database/db.sqlite3'

MIGRATION_DIR: Path = BASE_DIR / 'database/migrations/'

MODEL_DIR: Path = BASE_DIR / 'database/models/'
