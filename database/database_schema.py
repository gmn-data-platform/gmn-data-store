import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, ".env")))
db_uri = f'postgres://admin:{os.getenv("POSTGRES_ROOT_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
Base = declarative_base()


class Trajectory(Base):
    __tablename__ = 'trajectory'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

    # TODO: from data all definite data features into real data columns

    iau_code_id = Column(String(10), nullable=True, ForeignKey=('iau_code.id'))
    iau_code = relationship('IAUCode')

    station_id = Column(String(10), nullable=True, ForeignKey=('station.id'))
    station = relationship('Station')

    def __repr__(self):
        return f'<Trajectory {self.id}>'


class IAUCode(Base):
    __tablename__ = 'iau_code'
    id = Column(Integer, primary_key=True)  # same as IAU number
    code = Column(String(3), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('code'),)

    def __repr__(self):
        return f'<IAUCode {self.code}>'


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
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trajectory_id = Column(Integer, ForeignKey('trajectory.id'))
    station_id = Column(Integer, ForeignKey('station.id'))

    meteor = relationship('Trajectory', backref='recorded_by_station')
    station = relationship('Station', backref='meteors_recorded')

    __table_args__ = (UniqueConstraint('trajectory_id', 'station_id'),)

    def __repr__(self):
        return f'<ParticipatingStation {self.trajectory_id} {self.station_id}>'

# class StationCordinates(Base):
#     __table_name__ = 'station_cordinates'
#     id = Column(Integer, primary_key=True)
#
#     station_id = Column(Integer, ForeignKey('station.id'))
#     latitude = Column(String(255))
#     longitude = Column(String(255))
#     elevation = Column(String(255))
#
#     created_at = Column(DateTime, default=datetime.utcnow)
#     time_depedant_flag = Column(str, default=True)
