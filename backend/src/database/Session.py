from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.src.core.config import settings


engine = create_engine(settings.DATABASE_URL)
session = sessionmaker(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()