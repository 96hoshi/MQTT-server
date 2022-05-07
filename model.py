from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    chat_id = Column(String(100), unique=True)
    device = Column(Integer)
    alert_temp = Column(Boolean, default=False) # False = Led_spento/nessuna_notifica  True = Led_acceso/notifica_inviata


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    topic = Column(String(30))
    value = Column(Integer)
    timestamp = Column(DateTime)

#     # user = relationship("User", back_populates="device")

class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    device = Column(Integer)
    value = Column(Integer)
    timestamp = Column(DateTime)
