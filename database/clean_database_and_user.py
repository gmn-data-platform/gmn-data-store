#!/usr/bin/env python3
"""CAUTION! Removes $POSTGRES_DB."""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy_utils import drop_database

from . import get_engine, DB_URI

load_dotenv("/database/.env")

if __name__ == '__main__':
    if '-y' not in sys.argv and input(f'CAUTION! Are you sure you want to remove '
                                      f'database {os.getenv("POSTGRES_DATABASE")}'
                                      f'@{os.getenv("POSTGRES_HOST")}? (y/n) ') != "y":
        print("Exiting without action")
        exit()

    engine = get_engine()

    with engine.connect() as connection:
        drop_database(DB_URI)
        print("Dropped database")
