from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from model import Base, User, Device


engine = create_engine("sqlite://", echo=True, future=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)