from fast_five.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

settings = Settings()
engine = create_engine(settings.DATABASE_URL)


def get_session():
    yield Session(engine)
