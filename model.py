from numpy import integer
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    chat_id = Column(String(100), unique=True)
    alert_temp = Column(Boolean, default=False)
    alert_water = Column(Boolean, default=False)
    last_watered = Column(DateTime, default=None)


class Device(Base):
    __tablename__ = "device"

    name = Column(String(100), primary_key=True, unique=True)
    chat_id = Column(String(100), ForeignKey('user_account.chat_id'))


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(String(30), ForeignKey('device.name'))
    value = Column(Integer)
    timestamp = Column(DateTime)


class Humidity(Base):
    __tablename__ = "humidity"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    device = Column(String(30), ForeignKey('device.name'))
    value = Column(Integer)
    timestamp = Column(DateTime)


class Water(Base):
    __tablename__ = "water"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    device = Column(String(30), ForeignKey('device.name'))
    value = Column(Integer)
    timestamp = Column(DateTime)
