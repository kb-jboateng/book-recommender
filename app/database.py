from sqlmodel import create_engine, SQLModel, Session
from config import settings

__DB_URL = settings.DATABASE_URL

engine = create_engine(__DB_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session