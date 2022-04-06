"""This module stores the database models."""
from datetime import datetime

from gmn_python_api import get_trajectory_summary_avro_schema
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from gmn_data_store import get_engine

_Base = declarative_base()

_FIELDS_IN_TRAJECTORY_SUMMARY_NOT_METEOR_TABLE = [
    "unique_trajectory_identifier",
    "iau_no",
    "iau_code",
    "participating_stations",
    "num_stat",
]

_FIELDS_IN_METEOR_TABLE_NOT_TRAJECTORY_SUMMARY = [
    "id",
    "created_at",
    "updated_at",
    "iau_shower_id",
]


class Meteor(_Base):
    """Meteor table class."""

    __tablename__ = "meteor"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schema_version = Column(String, nullable=False)

    iau_shower_id = Column(Integer, ForeignKey("iau_shower.id"), nullable=True)
    iau_shower = relationship("IAUShower")

    def __repr__(self):
        """
        Return a string representation of the row.
        :return: string representation of the row.
        """
        return f"<Meteor {self.id}>"  # pragma: no cover


class IAUShower(_Base):
    """IAUShower table class."""

    __tablename__ = "iau_shower"
    id = Column(Integer, primary_key=True, autoincrement=False)  # same as IAU number
    code = Column(String(3), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("code"),)

    def __repr__(self):
        """
        Return a string representation of the row.
        :return: string representation of the row.
        """
        return (
            f"<IAUShower id={self.id}, code={self.code}," f" name={self.name}>"
        )  # pragma: no cover


class Station(_Base):
    """Station table class."""

    __tablename__ = "station"
    id = Column(Integer, primary_key=True)  # same as station number
    code = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("code"),)

    def __repr__(self):
        """
        Return a string representation of the row.
        :return: string representation of the row.
        """
        return f"<Station {self.code}>"  # pragma: no cover


class ParticipatingStation(_Base):
    """ParticipatingStation table class."""

    __tablename__ = "participating_station"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meteor_id = Column(String, ForeignKey("meteor.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("station.id"), nullable=False)

    meteor = relationship("Meteor", backref="recorded_by_station")
    station = relationship("Station", backref="meteors_recorded")

    __table_args__ = (UniqueConstraint("meteor_id", "station_id"),)

    def __repr__(self):
        """
        Return a string representation of the row.
        :return: string representation of the row.
        """
        return (
            f"<ParticipatingStation {self.meteor_id}" f" {self.station_id}>"
        )  # pragma: no cover


def _add_meteor_fields(engine, alter_table) -> None:
    """
    Add fields from the trajectory summary avsc schema to the meteor table.
    :param engine: SQLAlchemy engine.
    :return: None.
    """
    avsc = get_trajectory_summary_avro_schema()
    avro_type_to_sqlalchemy_type_map = {
        "null": None,
        "long": BigInteger,
        "double": Float,
        "string": String,
        "bytes": String,
        "boolean": Boolean,
        "int": Integer,
        "datetime": DateTime(timezone=False),
    }

    for field in avsc["fields"]:
        if (
            field["name"] in Meteor.__table__.columns.keys()
            or field["name"] in _FIELDS_IN_TRAJECTORY_SUMMARY_NOT_METEOR_TABLE
        ):
            continue

        nullable = False
        if field["type"][0] == "null":
            nullable = True

        logical_type = None

        # Special case for timestamp values
        if type(field["type"][1]) == dict:
            main_type = field["type"][1]["type"]
            if "logicalType" in field["type"][1]:
                logical_type = field["type"][1]["logicalType"]
        else:
            main_type = field["type"][1]

        if logical_type == "timestamp-micros":
            main_type = "datetime"

        column = Column(
            field["name"],
            avro_type_to_sqlalchemy_type_map[main_type],
            nullable=nullable,
        )
        _add_column(engine, "meteor", Meteor, column, alter_table)
        print(f"Added column if not exists {field['name']} type {main_type}")


def _add_column(engine, table_name, table_class, column, alter_table) -> None:
    """
    Add a column to a table and to the model.
    :param engine: SQLAlchemy engine
    :param table_name: Name of the table
    :param table_class: SQLAlchemy model class
    :param column: SQLAlchemy column
    :return: None
    """
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    try:
        if hasattr(table_class, str(column_name)):
            return

        if alter_table:
            engine.execute(
                "ALTER TABLE %s ADD COLUMN %s %s"
                % (table_name, column_name, column_type)
            )

        setattr(table_class, str(column_name), column)
        print(f"Added column if not exists {column_name} type {column_type}")
    except Exception as e:
        print(e)
        print(
            f"Couldn't create column {column_name}, it could already exist in the "
            f"database."
        )


engine = get_engine()
_add_meteor_fields(engine, alter_table=False)
