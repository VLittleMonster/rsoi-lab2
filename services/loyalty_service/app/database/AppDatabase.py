from config.config import get_db_url
from database.database import Database


class AppDatabase:
    app_db = Database(db_url=get_db_url())
