from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from api.config import get_settings

engine = create_engine(get_settings().database_url)


def get_session():
    with Session(engine) as session:
        yield session
