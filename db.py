from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from settings import DATABASE_URL

from sqlalchemy.pool import SingletonThreadPool

engine = create_engine(
    DATABASE_URL,
    poolclass=SingletonThreadPool,
)
session_maker = sessionmaker(bind=engine, autoflush=False)


def get_session(request: Request):
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
