from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    chat_id = Column(String)

    device = relationship(
        "Device", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, device={self.device!r})"

class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    hum = Column(Integer)
    temp = Column(Integer)
    water = Column(Integer)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="device")
    def __repr__(self):
        return f"Device(id={self.id!r}, timestamp={self.timestamp!r})"
