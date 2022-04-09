"""GMN Data Store."""
from pathlib import Path

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm import sessionmaker

_DB_DIRECTORY = f"{str(Path.home())}/.gmn_data_store/gmn_data_store.db"
_DB_CONNECTION_URI = f"sqlite:///{_DB_DIRECTORY}"


def get_engine() -> Engine:
    """
    Create an engine for the database.
    :return: The engine for the database.
    """
    return create_engine(_DB_CONNECTION_URI)


def get_session(engine: Engine) -> Session:
    """
    Generate sessions for making database queries.
    :return: A session for the database.
    """
    return sessionmaker(bind=engine)()
