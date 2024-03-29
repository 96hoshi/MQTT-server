import os
import json
import paho.mqtt.client as paho

from paho import mqtt
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot

from alert import Alert
from database import DBHandler


load_dotenv()

hostname = os.environ['HOSTNAME']
username = os.environ['SERVER_NAME']
password = os.environ['SERVER_PASSWORD']
token = os.environ['TOKEN']

MIN_TEMP = 15
MAX_TEMP = 35

bot = Bot(token=token)
db = DBHandler()


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# handle messages recieved
def on_message(client, userdata, msg):
    root, device, sensor = str(msg.topic).split("/")
    response_topic = "device/"+device+"/led"

    if not db.find_device(device):
        db.add_device(device)

    if not db.user_in_device(device):
        return

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    topic = msg.topic

    # The requested command is at the end of the topic
    if sensor == "dht":
        # parse payload
        payload = slice_payload(msg.payload)
        h, t = parse_dht(payload)
        user = db.get_user_by_device(device)


        if t > MIN_TEMP and t < MAX_TEMP:
            res = Alert.RED_OFF.value
            publish(client, response_topic, res, 0)
            if user is not None:
                if user.alert_temp:
                    # publish(client, response_topic, res, 1)
                    # bot.send_message(chat_id=chat_id, text='Temperature fine!')
                    db.set_OFF_temp_alarm(user)

        else:
            res = Alert.RED_ON.value
            publish(client, response_topic, res, 0)
            if user is not None:
                chat_id = user.chat_id
                if not user.alert_temp:
                    # publish(client, response_topic, res, 1)
                    if t < MIN_TEMP:
                        text = 'Temperature too low!'
                    else:
                        text = 'Temperature too high!'
                    bot.send_message(chat_id=chat_id, text=text)
                    db.set_ON_temp_alarm(user)

        if user is not None:
            now = datetime.utcnow()
            #store temperature in the db
            db.add_temperature(user.id, t, device, now)
            #store humidity in the db
            db.add_humidity(user.id, h, device, now)

    elif sensor == "water":
        # parse payload
        payload = slice_payload(msg.payload)
        value = parse_water(payload)
        user = db.get_user_by_device(device)

        if value == 1:
            res = Alert.BLUE_OFF.value
            publish(client, response_topic, res, 0)
            if user is not None:
                if user.alert_water:
                    # publish(client, response_topic, res, 1)
                    # bot.send_message(chat_id=chat_id, text='Water parameter good!')
                    db.set_OFF_water_alarm(user)
                    db.set_last_watered(user)
            
        elif value == 0:
            res = Alert.BLUE_ON.value
            publish(client, response_topic, res, 0)
            if user is not None:
                chat_id = user.chat_id
                if not user.alert_water:
                    # publish(client, response_topic, res, 1)
                    bot.send_message(chat_id=chat_id, text='Your plant needs some water!')
                    db.set_ON_water_alarm(user)

        if user is not None:
            now = datetime.utcnow()
            #store water in the db
            db.add_water(user.id, value, device, now)
    else:
        return


def slice_payload(payload):
    sliced = str(payload)[2:]
    return sliced[:len(sliced)-1]


def parse_dht(payload):
    h, t = payload.split(",")
    hum = int(h.split(":")[1])
    temp = int(t.split(":")[1])
    return hum, temp


def parse_water(payload):
    w = int(payload.split(":")[1])
    return w


def publish(client, topic, response, qos):
    # Now send the alert to the client
    print("Sending response "+str(response)+" on '"+topic+"'")

    payload = json.dumps(response)
    client.publish(topic, payload, qos=qos)


def main():
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = paho.Client(client_id="phao_plant_server", clean_session=True, userdata=None, protocol=paho.MQTTv31)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    if username:
        client.username_pw_set(username, password)

    # connect to HiveMQ Cloud on port 8883
    client.connect(hostname, 8883)
    client.subscribe("device/#", qos=0)
    client.loop_forever()

if __name__ == '__main__':
    main()
