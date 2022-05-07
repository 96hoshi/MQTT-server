import os
import time
import json
import paho.mqtt.client as paho

from paho import mqtt
from dotenv import load_dotenv
from alert import Alert
from telegram import Bot
from database import DBHandler


load_dotenv()

hostname = os.environ['HOSTNAME']
username = os.environ['SERVER_NAME']
password = os.environ['SERVER_PASSWORD']

MIN_TEMP = 15
MAX_TEMP = 35
MIN_LIGHT = 1000
MAX_LIGHT = 100000

TOKEN = os.environ['TOKEN']
bot = Bot(token=TOKEN)
dev = 1 #TODO: rimuovere var globale e sostituire con device dell'utente
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


def on_message(client, userdata, msg):
    global RED_IS_ON, BLUE_IS_ON
    response_topic = "plant/led"

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    topic = msg.topic

    # The requested command is at the end of the topic
    if topic.endswith("dht"):
        sliced = str(msg.payload)[2:]
        payload = sliced[:len(sliced)-1]

        h, t = parse_dht(payload)
        if t > MIN_TEMP and t < MAX_TEMP:
            res = Alert.RED_OFF.value
            publish(client, response_topic, res, 1)
            user = db.get_user_by_device(dev)
            if user is not None:
                # chat_id = user.chat_id
                if user.alert_temp:
                    # bot.send_message(chat_id=chat_id, text='Temperature fine!') #TODO: completare
                    db.set_OFF_temp_alarm(user)
            # send_message("Temperature alert!")
            # TODO put it in a database and associate it with the client_id
        else:
            res = Alert.RED_ON.value
            publish(client, response_topic, res, 1)
            user = db.get_user_by_device(dev)
            if user is not None:
                chat_id = user.chat_id
                if not user.alert_temp:
                    bot.send_message(chat_id=chat_id, text='Temperature too high!') #TODO: completare
                    db.set_ON_temp_alarm(user)

    elif topic.endswith("water"):
        sliced = str(msg.payload)[2:]
        payload = sliced[:len(sliced)-1]

        value = parse_water(payload)
        if value == 1:
            res = Alert.BLUE_OFF.value
            publish(client, response_topic, res, 1)
            # TODO put it in a database and associate it with the client_id
        elif value == 0:
            res = Alert.BLUE_ON.value
            publish(client, response_topic, res, 1)
            # TODO: send message to bot
    else:
        return

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def parse_dht(payload):
    print(payload)
    h, t = payload.split(",")
    hum = int(h.split(":")[1])
    temp = int(t.split(":")[1])

    return hum, temp

def parse_water(payload):
    print(payload)
    w = int(payload.split(":")[1])

    return w

def publish(client, topic, response, qos):
    # Now send the alert to the client led
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

    # connect to HiveMQ Cloud on default port 8883
    client.connect(hostname, 8883)
    client.subscribe("plant/#", qos=0)
    client.loop_forever()


if __name__ == '__main__':
    main()
