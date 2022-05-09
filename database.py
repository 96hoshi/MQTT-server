from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import timedelta, datetime

from model import Base, Humidity, User, Temperature, Water, Device


class DBHandler:
    def __init__(self):
        self.engine = create_engine("sqlite:///plant.db", echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add_user(self, name, chat_id):
        new_user = User()
        new_user.name = name
        new_user.chat_id = chat_id
        self.session.add(new_user)
        self.session.commit()

    def add_device(self, name):
        new_device = Device()
        new_device.name = name
        new_device.chat_id = None
        self.session.add(new_device)
        self.session.commit()

    def add_temperature(self, user_id, value, device, timestamp):
        new_temp = Temperature()
        new_temp.value = value
        new_temp.user_id = user_id
        new_temp.device = device
        new_temp.timestamp = timestamp
        self.session.add(new_temp)
        self.session.commit()

    def add_humidity(self, user_id, value, device, timestamp):
        new_hum = Humidity()
        new_hum.value = value
        new_hum.user_id = user_id
        new_hum.device = device
        new_hum.timestamp = timestamp
        self.session.add(new_hum)
        self.session.commit()

    def add_water(self, user_id, value, device, timestamp):
        new_water = Water()
        new_water.value = value
        new_water.user_id = user_id
        new_water.device = device
        new_water.timestamp = timestamp
        self.session.add(new_water)
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

    def set_last_watered(self, user):
        user.last_watered = datetime.utcnow()
        self.session.commit()

    def get_last_watered(self, chat_id):
        usr = self.get_user_by_chat_id(chat_id)
        if usr is None:
            return usr
        return usr.last_watered

    def add_chat_id_to_device(self, device, chat_id):
        dev = self.get_device(device)
        if dev is None:
            return None
        if dev.chat_id is None:
            dev.chat_id = chat_id
            self.session.commit()
            return True
        return False

    def get_device(self, name):
        return self.session.query(Device).filter(Device.name == name).first()

    def get_dev_name_by_chat_id(self, chat_id):
        dev = self.session.query(Device).filter(Device.chat_id == chat_id).first()
        if dev:
            return dev.name
        return None

    def get_status(self, chat_id, dev):
        MIN_HUM = 20
        MAX_HUM = 80

        usr = self.get_user_by_chat_id(chat_id)
        if usr is None:
            return None

        hum = self.get_last_humidity(dev)
        hum_status = "not detected"
        if hum is not None:
            if hum.value >= MIN_HUM and hum.value <= MAX_HUM:
                hum_status = "optimal"
            else:
                hum_status = "not ideal"
        return [usr.alert_temp, usr.alert_water, hum_status]

    def user_in_device(self, name):
        dev = self.session.query(Device).filter(Device.name == name).first()
        if dev is None:
            return False

        if dev.chat_id is None:
            return False
        return True 

    def find_user(self, chat_id):
        return self.session.query(User).filter(User.chat_id == chat_id).first() is not None

    def find_device(self, name):
        return self.session.query(Device).filter(Device.name == name).first() is not None

    def get_user_by_device(self, name):
        dev = self.session.query(Device).filter(Device.name == name).first()
        if dev is None:
            return dev
        return self.session.query(User).filter(User.chat_id == dev.chat_id).first() 


    def get_user_by_chat_id(self, chat_id):
        return self.session.query(User).filter(User.chat_id == chat_id).first()

    def get_last_temperature(self, device):
        return self.session.query(Temperature).filter(Temperature.device == device).order_by(Temperature.timestamp.desc()).first()

    def get_last_humidity(self, device):
        return self.session.query(Humidity).filter(Humidity.device == device).order_by(Humidity.timestamp.desc()).first()

    def get_last_water(self, device):
        return self.session.query(Water).filter(Water.device == device).order_by(Water.timestamp.desc()).first()

    def get_avg_temperature(self, device):
        time_now = datetime.utcnow()
        last_hour = time_now - timedelta(hours=1)
        avg = self.session.query(func.avg(Temperature.value).label('average'))\
                        .filter(Temperature.device == device)\
                        .filter(Temperature.timestamp >= last_hour)\
                        .first()
        return avg.average

    def get_avg_humidity(self, device):
        time_now = datetime.utcnow()
        last_hour = time_now - timedelta(hours=1)
        avg = self.session.query(func.avg(Humidity.value).label('average'))\
                        .filter(Humidity.device == device)\
                        .filter(Humidity.timestamp >= last_hour)\
                        .first()
        return avg.average
