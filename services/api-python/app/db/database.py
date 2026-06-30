from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

#Singleton pattern for database engine and session: Only one engine and connection pool per process.
class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.engine = create_engine(
                settings.database_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )

            cls._instance.SessionLocal = sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=cls._instance.engine,
            )

        return cls._instance


db_manager = DatabaseManager()

Base = declarative_base()


def get_db():
    db = db_manager.SessionLocal()

    try:
        yield db
    finally:
        db.close()