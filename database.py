from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session

from model import Base, User, Device

class DBHandler:
    def __init__(self):
        self.engine = create_engine("sqlite:///plant.db", echo=True, future=True)
        # if not database_exists(self.engine.url):
        #     create_database(self.engine.url)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        print("db-handler")

    def add_User(self, name, chat_id):
        new_user = User()
        new_user.name = name
        new_user.chat_id = chat_id

        self.session.add(new_user)
        self.session.commit()
