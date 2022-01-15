import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, ".env")))
db_uri = f'postgres://admin:{os.getenv("POSTGRES_ROOT_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
Base = declarative_base()


class Trajectory(Base):
    __tablename__ = 'trajectory'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Beginning(UTC Time)
    # Beginning (Julian date)
    # IAU(No)
    # Sol lon(deg)
    # App LST(deg)
    # RAgeo(deg)
    # + / - (sigma)
    # DECgeo(deg)
    # + / - (sigma.1)
    # LAMgeo(deg)
    # + / - (sigma.2)
    # BETgeo(deg)
    # + / - (sigma.3)
    # Vgeo(km / s)
    # + / - (sigma.4)
    # LAMhel(deg)
    # + / - (sigma.5)
    # BEThel(deg)
    # + / - (sigma.6)
    # Vhel(km / s)
    # + / - (sigma.7)
    # a(AU)
    # + / - (sigma.8)
    # e
    # + / - (sigma.9)
    # i(deg)
    # + / - (sigma.10)
    # peri(deg)
    # + / - (sigma.11)
    # node(deg)
    # + / - (sigma.12)
    # Pi(deg)
    # + / - (sigma.13)
    # b(deg)
    # + / - (sigma.14)
    # q(AU)
    # + / - (sigma.15)
    # f(deg)
    # + / - (sigma.16)
    # M(deg)
    # + / - (sigma.17)
    # Q(AU)
    # + / - (sigma.18)
    # n(deg / day)
    # + / - (sigma.19)
    # T(years)
    # + / - (sigma.20)
    # TisserandJ
    # + / - (sigma.21)
    # RAapp(deg)
    # + / - (sigma.22)
    # DECapp(deg)
    # + / - (sigma.23)
    # Azim + E(of N deg)
    # + / - (sigma.24)
    # Elev(deg)
    # + / - (sigma.25)
    # Vinit(km / s)
    # + / - (sigma.26)
    # Vavg(km / s)
    # + / - (sigma.27)
    # LatBeg(+N deg)
    # + / - (sigma.28)
    # LonBeg(+E deg)
    # + / - (sigma.29)
    # HtBeg(km)
    # + / - (sigma.30)
    # LatEnd(+N deg)
    # + / - (sigma.31)
    # LonEnd(+E deg)
    # + / - (sigma.32)
    # HtEnd(km)
    # + / - (sigma.33)
    # Duration(sec)
    # Peak(AbsMag)
    # Peak Ht(km)
    # F(param)
    # Mass kg(tau=0.7 %)
    # Qc(deg)
    # MedianFitErr(arcsec)
    # Beg in (FOV)
    # End in (FOV)
    # Num(stat)

class IAUCode(Base):
    __tablename__ = 'iau_code'
    id = Column(Integer, primary_key=True) # same as IAU number
    code = Column(String(3), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('code'),)

class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True) # same as station number
    code = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # latitude = Column(String(255))
    # longitude = Column(String(255))
    # elevation = Column(String(255))
    # is_active = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint('code'),)

class StationCordinates(Base):
    __table_name__ = 'station_cordinates'
    id = Column(Integer, primary_key=True)

    station_id = Column(Integer, ForeignKey('station.id'))
    latitude = Column(String(255))
    longitude = Column(String(255))
    elevation = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)
    time_depedant_flag = Column(str, default=True)


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
