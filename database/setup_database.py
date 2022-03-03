#!/usr/bin/env python3
"""Creates $POSTGRES_DB for $POSTGRES_USER and setups up tables."""

import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

from . import DB_URI, get_engine
from database_schema import Base

load_dotenv("/database/.env")

if __name__ == '__main__':
    if not database_exists(DB_URI):
        create_database(DB_URI)
    print(f"Created database {os.getenv('POSTGRES_USER')} if it didn't exist.")

    Base.metadata.create_all(get_engine())
    print("Created tables")
