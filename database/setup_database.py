#!/usr/bin/env python3
"""Creates $POSTGRES_DB and setups up tables."""

import os
from dotenv import load_dotenv
from gmn_python_api import get_iau_showers
from sqlalchemy_utils import database_exists, create_database

from __init__ import DB_URI, get_engine
from controller import DatabaseController
from models import Base, IAUShower, add_trajectory_fields

load_dotenv("/database/.env")

def seed_data():
    initial_iau_showers = list(get_iau_showers().values())
    print(f"Initialising database with IAU showers {initial_iau_showers}")

    db_controller = DatabaseController()
    for fields in initial_iau_showers:
        db_controller.create_row(IAUShower, **fields)


if __name__ == '__main__':
    if not database_exists(DB_URI):
        create_database(DB_URI)
    print(f"Created database {os.getenv('POSTGRES_DB')} if it didn't exist.")

    engine = get_engine()
    Base.metadata.create_all(engine)
    add_trajectory_fields(engine)
    print("Created tables")

    seed_data()
    print("Populated with initial data")
