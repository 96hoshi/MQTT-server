from sqlalchemy import create_engine
#from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import timedelta, datetime

from model import Base, Humidity, User, Temperature, Water

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

    def set_ON_water_alarm(self, user):
        user.alert_water = True
        self.session.commit()

    def set_OFF_water_alarm(self, user):
        user.alert_water = False
        self.session.commit()

    def find_user(self, chat_id):
        return self.session.query(User).filter(User.chat_id == chat_id).first() is not None

    def get_user_by_device(self, device):
        return self.session.query(User).filter(User.device == device).first()
 
    def add_humidity(self, user_id, value, device, timestamp):
        new_hum = Humidity()
        new_hum.value = value
        new_hum.user_id = user_id
        new_hum.device = device
        new_hum.timestamp = timestamp

        self.session.add(new_hum)
        self.session.commit()

    def add_temperature(self, user_id, value, device, timestamp):
        new_temp = Temperature()
        new_temp.value = value
        new_temp.user_id = user_id
        new_temp.device = device
        new_temp.timestamp = timestamp

        self.session.add(new_temp)
        self.session.commit()

    def add_water(self, user_id, value, device, timestamp):
        new_water = Water()
        new_water.value = value
        new_water.user_id = user_id
        new_water.device = device
        new_water.timestamp = timestamp

        self.session.add(new_water)
        self.session.commit()

    def get_last_Water(self, device):
        return self.session.query(Water).filter(Water.device == device).order_by(Water.timestamp.desc()).first()

    def get_last_Humidity(self, device):
        return self.session.query(Humidity).filter(Humidity.device == device).order_by(Humidity.timestamp.desc()).first()

    def get_last_Temperature(self, device):
        return self.session.query(Temperature).filter(Temperature.device == device).order_by(Temperature.timestamp.desc()).first()

    def get_avg_Temperature(self, device):
        time_now = datetime.utcnow()
        last_hour = time_now - timedelta(hours=1)
        avg = self.session.query(func.avg(Temperature.value).label('average')).filter(Temperature.device == device).filter(Temperature.timestamp >= last_hour).filter(Temperature.timestamp <= time_now ).first()
        return avg.average

    # def get_last_Humidity(self, device):
    #     return self.session.query(Humidity).filter(Humidity.device == device).order_by(Humidity.timestamp.desc()).first()

    # def get_avg_Humidity(self, device):
    #     return self.session.query(func.avg(Humidity.value).label('average'))
