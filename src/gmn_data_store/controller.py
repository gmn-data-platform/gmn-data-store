"""This module contains functions for getting, updating and inserting into the database."""
import datetime
from typing import Any
from typing import Dict
from typing import Optional

import gmn_python_api
from sqlalchemy.engine import Engine  # type: ignore

from gmn_data_store import get_engine
from gmn_data_store import get_session
from gmn_data_store.models import _Base
from gmn_data_store.models import _FIELDS_IN_METEOR_TABLE_NOT_TRAJECTORY_SUMMARY
from gmn_data_store.models import _FIELDS_IN_TRAJECTORY_SUMMARY_NOT_METEOR_TABLE
from gmn_data_store.models import Meteor
from gmn_data_store.models import ParticipatingStation
from gmn_data_store.models import Station

_database = get_engine()


def create_row(
    table: _Base, fields: Dict[str, Any], engine: Optional[Engine] = None
) -> None:
    """
    Creates a row in a table.

    :param table: The table to add the row to.
    :param fields: A dictionary of fields to add to the table.

    :return: None
    """
    db_session = get_session(engine)
    row = table(**fields)
    exists = db_session.query(table).filter_by(id=fields["id"]).first()
    if not exists:
        db_session.add(row)
    db_session.commit()
    db_session.close()


def insert_trajectory_summary(
    trajectory_summary_avro: Dict[str, Any], engine: Optional[Engine] = None
) -> None:
    """
    Insert a row into the meteor table using a trajectory summary avro dictionary.

    :param trajectory_summary: A trajectory summary avro formatted dictionary that
     conforms to the official avsc schema.

    :return: None.
    """
    if not engine:  # pragma: no cover
        engine = get_engine()

    db_session = get_session(engine)
    schema = gmn_python_api.meteor_summary_schema.get_meteor_summary_avro_schema()
    timestamp_fields = [
        item["name"]  # type: ignore
        for item in schema["fields"]
        if item["type"]  # type: ignore
        == ["null", {"type": "long", "logicalType": "timestamp-micros"}]
    ]

    meteor_fields = {}  # fields to add to Meteor table
    for field in Meteor.__table__.columns.keys():
        if (
            field not in _FIELDS_IN_METEOR_TABLE_NOT_TRAJECTORY_SUMMARY
            and field not in _FIELDS_IN_TRAJECTORY_SUMMARY_NOT_METEOR_TABLE
        ):
            meteor_fields[field] = trajectory_summary_avro[field]

            # Special case for converting epoch microseconds to Datetime
            if field in timestamp_fields and type(meteor_fields[field]) == int:
                meteor_fields[field] = datetime.datetime.fromtimestamp(
                    meteor_fields[field] / 1e6
                )

    meteor_row = db_session.merge(
        Meteor(
            id=trajectory_summary_avro["unique_trajectory_identifier"],
            iau_shower_id=None
            if trajectory_summary_avro["iau_no"] == -1
            else trajectory_summary_avro["iau_no"],
            **meteor_fields
        )
    )
    db_session.commit()

    for station_code in trajectory_summary_avro["participating_stations"]:
        # If a station doesn't exist in the db with the same station_code
        existing_station = (
            db_session.query(Station).filter_by(code=station_code).first()
        )
        if not existing_station:
            station_row = db_session.merge(Station(code=station_code))
            db_session.commit()
            station_id = station_row.id
        else:
            station_id = existing_station.id

        if (  # pragma: no cover
            not db_session.query(ParticipatingStation)
            .filter_by(meteor_id=meteor_row.id, station_id=station_id)
            .first()
        ):
            db_session.merge(
                ParticipatingStation(meteor_id=meteor_row.id, station_id=station_id)
            )
            db_session.commit()

    db_session.close()
