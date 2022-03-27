from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

Base = declarative_base()

SCHEMA_VERSION = "2.0"
AVSC_PATH = "/avro/trajectory_summary_schema_2.0.avsc"

class Trajectory(Base):
    __tablename__ = 'trajectory'
    id = Column(String, primary_key=True)
    # meteor_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Basic properties that define a meteor
    beginning_utc_time = Column(DateTime(timezone=False), nullable=False)
    latbeg_n_deg = Column(Float, nullable=False)
    lonbeg_e_deg = Column(Float, nullable=False)
    htbeg_km = Column(Float, nullable=False)
    rageo_deg = Column(Float, nullable=False)
    decgeo_deg = Column(Float, nullable=False)
    vgeo_km_s = Column(Float, nullable=False)

    # Extra trajectory properties calculated from the meteor properties
    data = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False) # {...}
    schema_version = Column(String, nullable=False)

    # IAU shower relation
    iau_shower_id = Column(Integer, ForeignKey('iau_shower.id'), nullable=True)
    iau_shower = relationship('IAUShower')

    # __table_args__ = (UniqueConstraint('meteor_id'),)

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
