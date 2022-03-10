#!/usr/bin/env python3
"""Creates $POSTGRES_DB and setups up tables."""

import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

from __init__ import DB_URI, get_engine
from controller import DatabaseController
from database_schema import Base, IAUCode, Station

load_dotenv("/database/.env")

def seed_data():
    initial_stations = [ # https://github.com/wmpg/WesternMeteorPyLib/blob/master/wmpl/Utils/ShowerAssociation.py#L116
        # streamfulldata.csv 2nd col=iau_no, code, name, use first occurrence
        {'id': 1, 'code': "UK001"},
        {'id': 2, 'code': "UK002"},
        {'id': 4, 'code': "FR004"},
    ]
    initial_iau_showers = [ #
        {'id': 1, 'code': "CAP"},
        {'id': 2, 'code': "STA"},
        {'id': 4, 'code': "GEM"},
    ]

    db_controller = DatabaseController()

    for fields in initial_stations:
        db_controller.create_row(Station, **fields)

    for fields in initial_iau_showers:
        db_controller.create_row(IAUCode, **fields)


if __name__ == '__main__':
    if not database_exists(DB_URI):
        create_database(DB_URI)
    print(f"Created database {os.getenv('POSTGRES_DB')} if it didn't exist.")

    Base.metadata.create_all(get_engine())
    print("Created tables")

    seed_data()
    print("Populated with initial data")
