import peewee

import settings

database = peewee.SqliteDatabase(settings.BASE_DIR / 'database/db.sqlite3')
