from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

Base = declarative_base()


class Trajectory(Base):
    __tablename__ = 'trajectory'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

    # TODO: from data all definite data features into real data columns

    iau_code_id = Column(Integer, ForeignKey('iau_code.id'), nullable=False)
    iau_code = relationship('IAUCode')

    station_id = Column(Integer, ForeignKey('station.id'), nullable=False)
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

    trajectory_id = Column(Integer, ForeignKey('trajectory.id'), nullable=False)
    station_id = Column(Integer, ForeignKey('station.id'), nullable=False)

    meteor = relationship('Trajectory', backref='recorded_by_station')
    station = relationship('Station', backref='meteors_recorded')

    __table_args__ = (UniqueConstraint('trajectory_id', 'station_id'),)

    def __repr__(self):
        return f'<ParticipatingStation {self.trajectory_id} {self.station_id}>'

# class StationCoordinates(Base):
#     __table_name__ = 'station_coordinates'
#     id = Column(Integer, primary_key=True)
#
#     station_id = Column(Integer, ForeignKey('station.id'))
#     latitude = Column(String(255))
#     longitude = Column(String(255))
#     elevation = Column(String(255))
#
#     created_at = Column(DateTime, default=datetime.utcnow)
#     time_depedant_flag = Column(str, default=True)
