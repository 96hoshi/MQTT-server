from numpy import integer
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    chat_id = Column(String(100), unique=True)
    device = Column(Integer)
    alert_temp = Column(Boolean, default=False)
    alert_water = Column(Boolean, default=False)
    last_watered = Column(DateTime, default=None)


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    device = Column(Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)


class Humidity(Base):
    __tablename__ = "humidity"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    device = Column(Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)


class Water(Base):
    __tablename__ = "water"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    device = Column(Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)
