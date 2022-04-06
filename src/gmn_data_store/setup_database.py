#!/usr/bin/env python3
"""This module creates database and setups up tables."""

from gmn_python_api import get_iau_showers
from sqlalchemy.engine import Engine

from gmn_data_store import get_engine
from gmn_data_store import controller
from gmn_data_store.models import _Base, IAUShower, _add_meteor_fields


def setup_database() -> Engine:
    """
    Setup database, tables and seed data.
    :return: None
    """
    engine = get_engine()
    _Base.metadata.create_all(engine)
    _add_meteor_fields(engine, alter_table=True)
    print("Created tables")

    seed_data(engine)
    print("Populated with initial data")
    return engine

def seed_data(engine) -> None:
    """
    Seed data into database.
    :param engine: SQLAlchemy engine.
    :return: None.
    """
    initial_iau_showers = list(get_iau_showers().values())
    print(f"Initialising gmn-data-store with IAU showers {initial_iau_showers}")

    for fields in initial_iau_showers:
        controller.create_row(IAUShower, fields, engine=engine)


if __name__ == '__main__':
    setup_database() # pragma: no cover
