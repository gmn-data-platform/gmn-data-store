"""GMN Data Store."""
from pathlib import Path
from sqlite3 import Connection

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy import event
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import _ConnectionRecord  # type: ignore

_DB_DIRECTORY = f"{str(Path.home())}/.gmn_data_store/gmn_data_store.db"
_DB_CONNECTION_URI = f"sqlite:///{_DB_DIRECTORY}"


def get_engine() -> Engine:
    """
    Create an engine for the database.

    :return: The engine for the database.
    """
    engine = create_engine(_DB_CONNECTION_URI)
    event.listen(engine, "connect", _pragma_on_connect)
    return engine


def get_session(engine: Engine) -> Session:
    """
    Generate sessions for making database queries.

    :return: A session for the database.
    """
    return sessionmaker(bind=engine)()


def _pragma_on_connect(
    dbapi_connection: Connection, connection_record: _ConnectionRecord
) -> None:
    """
    Enable Write-Ahead Logging for concurrent access.

    :param dbapi_connection: The database connection.
    :param connection_record: The connection record.

    :return: None.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode = WAL")
    cursor.close()
