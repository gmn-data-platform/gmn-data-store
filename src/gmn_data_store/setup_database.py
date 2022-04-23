#!/usr/bin/env python3
"""This module creates database and setups up tables."""
from gmn_python_api import get_meteor_summary_avro_schema  # type: ignore
from gmn_python_api.iau_showers import get_iau_showers
from sqlalchemy import Table  # type: ignore
from sqlalchemy import text
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy_views import CreateView  # type: ignore
from sqlalchemy_views import DropView

from gmn_data_store import controller
from gmn_data_store import get_engine
from gmn_data_store.models import _add_meteor_fields
from gmn_data_store.models import _Base
from gmn_data_store.models import IAUShower


def setup_database() -> Engine:
    """
    Setup database, tables and seed data.

    :return: None
    """
    engine = get_engine()
    _Base.metadata.create_all(engine)
    _add_meteor_fields(engine, alter_table=True)
    create_meteor_summary_view(engine)
    print("Created tables")

    seed_data(engine)
    print("Populated with initial data")
    return engine


def create_meteor_summary_view(engine: Engine) -> None:
    """
    Create a flat meteor summary view from the related meteor tables.

    :param engine: SQLAlchemy engine.
    :param meteor_columns: List of columns from the meteor table.

    :return: None.
    """
    special_select_fields = {
        "unique_trajectory_identifier": "meteor.id AS unique_trajectory_identifier",
        "iau_no": "iau_shower.id AS iau_no",
        "iau_code": "iau_shower.code AS iau_code",
        "num_stat": "count(station.id) AS num_stat",
        "participating_stations": "GROUP_CONCAT(station.code) AS participating_stations",
    }
    schema = get_meteor_summary_avro_schema()
    columns = []
    for field in schema["fields"]:
        if field["name"] in special_select_fields:
            columns.append(special_select_fields[field["name"]])
        else:
            columns.append(field["name"])

    columns_str = ",\n  ".join(columns)
    query = f"""SELECT
      {columns_str}
    FROM
      meteor
      LEFT JOIN iau_shower on meteor.iau_shower_id = iau_shower.id
      LEFT JOIN participating_station ON participating_station.meteor_id = meteor.id
      LEFT JOIN station ON participating_station.station_id = station.id
    GROUP BY meteor.id"""

    view = Table("meteor_summary", _Base.metadata)
    drop_view = DropView(view, if_exists=True)
    drop_view.execute(engine)
    definition = text(query)
    create_view = CreateView(view, definition)
    create_view.execute(engine)
    print("Created or replaced views")


def seed_data(engine: Engine) -> None:
    """
    Seed data into database.

    :param engine: SQLAlchemy engine.

    :return: None.
    """
    initial_iau_showers = list(get_iau_showers().values())
    for fields in initial_iau_showers:
        controller.create_row(IAUShower, fields, engine=engine)


if __name__ == "__main__":
    setup_database()  # pragma: no cover
