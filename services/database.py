from contextlib import contextmanager

from config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"  # noqa

engine = create_engine(POSTGRES_URL, echo=True)

session = sessionmaker(autoflush=True, autocommit=False, bind=engine)

Base = declarative_base()


@contextmanager
def create_session():
    ss = session()
    try:
        yield ss
    finally:
        ss.close()


async def get_db():
    with create_session() as session:
        yield session
