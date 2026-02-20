import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    os.makedirs("data", exist_ok=True)
    engine = create_engine(settings.database_url, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    from app.db import models  # noqa
    Base.metadata.create_all(bind=engine)

def get_db():
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()