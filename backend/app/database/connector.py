from sqlalchemy import engine
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_app_settings

settings = get_app_settings()

sqlUrl = engine.url.URL.create(
    drivername="postgresql+psycopg2",
    username=settings.db_user,
    password=settings.db_pass,
    host=settings.db_host,
    port=5432,
    database=settings.db_name,
)

metadata = MetaData()

engine = create_engine(
    sqlUrl,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
