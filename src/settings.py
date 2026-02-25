from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent

DATABASE_FILE: Path = BASE_DIR / 'database/db.sqlite3'
