from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session

from model import Base, User, Device, Temperature

class DBHandler:
    def __init__(self):
        self.engine = create_engine("sqlite:///plant.db", echo=True, future=True)
        # if not database_exists(self.engine.url):
        #     create_database(self.engine.url)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        print("db-handler")

    def add_User(self, name, chat_id, device):
        new_user = User()
        new_user.name = name
        new_user.chat_id = chat_id
        new_user.device = device

        self.session.add(new_user)
        self.session.commit()

    def set_ON_temp_alarm(self, user):
        user.alert_temp = True
        self.session.commit()

    def set_OFF_temp_alarm(self, user):
        user.alert_temp = False
        self.session.commit()

    def find_user(self, chat_id):
        return self.session.query(User).filter(User.chat_id == chat_id).first() is not None

    def get_user_by_device(self, device):
        return self.session.query(User).filter(User.device == device).first()

    def add_Temperature(self, value, device, timestamp):
        new_temp = Temperature()
        new_temp.value = value
        new_temp.device = device
        new_temp.timestamp = timestamp

        self.session.add(new_temp)
        self.session.commit()

    def get_last_Temperature(self, device):
        return self.session.query(Temperature).filter(Temperature.device == device).order_by(Temperature.timestamp.desc()).first()
