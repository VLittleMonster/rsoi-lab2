from database.database import Database
from config.config import get_db_url


class AppDatabase:
    app_db = Database(db_url=get_db_url())
