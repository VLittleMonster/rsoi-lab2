from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    def __init__(self, db_url):
        self.DB_URL = db_url

        if db_url[:6] != "sqlite":
            self.engine = create_engine(self.DB_URL)
        else:
            self.engine = create_engine(self.DB_URL, connect_args={"check_same_thread": False})        #
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close_all()
