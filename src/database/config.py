import peewee

import settings

database = peewee.SqliteDatabase(settings.DATABASE_FILE)
