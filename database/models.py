from datetime import datetime

from gmn_python_api import get_trajectory_summary_avro_schema
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime,\
    BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

SCHEMA_VERSION = "2.0"
AVSC_PATH = "/avro/trajectory_summary_schema_2.0.avsc"

class Trajectory(Base):
    __tablename__ = 'trajectory'
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schema_version = Column(String, nullable=False)

    iau_shower_id = Column(Integer, ForeignKey('iau_shower.id'), nullable=True)
    iau_shower = relationship('IAUShower')

    def __repr__(self):
        return f'<Trajectory {self.id}>'


class IAUShower(Base):
    __tablename__ = 'iau_shower'
    id = Column(Integer, primary_key=True, autoincrement=False)  # same as IAU number
    code = Column(String(3), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('code'),)

    def __repr__(self):
        return f'<IAUShower id={self.id}, code={self.code}, name={self.name}>'


class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)  # same as station number
    code = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('code'),)

    def __repr__(self):
        return f'<Station {self.code}>'


class ParticipatingStation(Base):
    __tablename__ = 'participating_station'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trajectory_id = Column(String, ForeignKey('trajectory.id'), nullable=False)
    station_id = Column(Integer, ForeignKey('station.id'), nullable=False)

    meteor = relationship('Trajectory', backref='recorded_by_station')
    station = relationship('Station', backref='meteors_recorded')

    __table_args__ = (UniqueConstraint('trajectory_id', 'station_id'),)

    def __repr__(self):
        return f'<ParticipatingStation {self.trajectory_id} {self.station_id}>'


def add_trajectory_fields(engine):
    avsc = get_trajectory_summary_avro_schema()
    print(avsc)
    avro_type_to_sqlalchemy_type_map = {
        'null': None,
        'long': BigInteger,
        'double': Float,
        'string': String,
        'bytes': String,
        'boolean': Boolean,
        'int': Integer,
        'datetime': DateTime(timezone=False),
    }

    trajectory_table_exclude_fields = [
        'unique_trajectory_identifier'
        'iau_no',
        'iau_code',
        'participating_stations',
        'num_stat'
    ]

    for field in avsc["fields"]:
        if field["name"] in Trajectory.__dict__:
            continue
        if field["name"] in trajectory_table_exclude_fields:
            continue

        nullable = False
        if field["type"][0] == "null":
            nullable = True

        logical_type = None

        if type(field["type"][1]) == dict:
            main_type = field["type"][1]["type"]
            if "logical_type" in field["type"][1]:
                logical_type = field["type"][1]["logicalType"]
        else:
            main_type = field["type"][1]

        if logical_type == "timestamp-micros":
            main_type = "datetime"

        column = Column(field["name"], avro_type_to_sqlalchemy_type_map[main_type], nullable=nullable)
        add_column(engine, "trajectory", column)
        print(f"Added column {field['name']} type {main_type}")


# https://stackoverflow.com/questions/7300948/add-column-to-sqlalchemy-table
def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))
