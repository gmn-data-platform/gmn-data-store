""""""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv("/database/.env")

DB_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:' \
         f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:' \
         f'{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'


def get_engine():
    return create_engine(DB_URI, pool_size=50, echo=False)


def get_session():
    return sessionmaker(bind=get_engine())()
