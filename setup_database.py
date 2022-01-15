#!/usr/bin/env python3
"""Creates and populates $POSTGRES_DATABASE, and $POSTGRES_USER with access rights to the database."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from database_schema import Base

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, ".env")))
db_uri = f'postgres://admin:{os.getenv("POSTGRES_ROOT_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'



if __name__ == '__main__':
    engine = create_engine(db_uri)

    with engine.connect() as connection:
        connection.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("POSTGRES_DATABASE")}')
        print("Added database-cli")

        connection.execute(f'CREATE USER IF NOT EXISTS {os.getenv("POSTGRES_USER")}@{os.getenv("POSTGRES_HOST")} '
                           f'IDENTIFIED BY \'{os.getenv("POSTGRES_PASSWORD")}\'')
        print("Created user")

        connection.execute(f'GRANT ALL PRIVILEGES ON {os.getenv("POSTGRES_DATABASE")}.* '
                           f'TO {os.getenv("POSTGRES_USER")}@{os.getenv("POSTGRES_HOST")}')
        print("Granted privileges")

    engine = create_engine(f'{db_uri}/{os.getenv("POSTGRES_DATABASE")}')
    Base.metadata.create_all(engine)
    print("Created tables")

    # seed_data()
    # print("Populated with initial data")