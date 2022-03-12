#!/usr/bin/env python3
"""Creates $POSTGRES_DB and setups up tables."""

import os
import requests
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

from __init__ import DB_URI, get_engine
from controller import DatabaseController
from models import Base, IAUShower

IAU_SHOWERS_LIST = "https://www.ta3.sk/IAUC22DB/MDC2007/Etc/streamfulldata.txt"

load_dotenv("/database/.env")


def get_iau_showers():
    r = requests.get(IAU_SHOWERS_LIST)
    r.raise_for_status()

    showers = {}
    for row in r.text.splitlines():
        if not row or row.startswith(":") or row.startswith("+"):
            continue

        row_values = row.split("|")

        shower_no = row_values[1].strip('" ')
        if shower_no in showers:
            continue

        shower_code = row_values[3].strip('" ')
        shower_name = row_values[4].strip('" ')

        showers[shower_no] = {
            "id": shower_no,
            "code": shower_code,
            "name": shower_name
        }

    return showers


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

    Base.metadata.create_all(get_engine())
    print("Created tables")

    seed_data()
    print("Populated with initial data")
