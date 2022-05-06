# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import time
import json
import paho.mqtt.client as paho

from paho import mqtt
from dotenv import load_dotenv

from alert import Alert


load_dotenv()

hostname = os.environ['HOSTNAME']
username = os.environ['SERVER_NAME']
password = os.environ['SERVER_PASSWORD']

MIN_TEMP = 15
MAX_TEMP = 35
MIN_LIGHT = 1000
MAX_LIGHT = 100000

# TODO put it in a database and associate it with the client_id
RED_IS_ON = False
BLUE_IS_ON = False


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

    topic = msg.topic
    value = float(msg.payload.decode("utf-8"))

    # The requested command is at the end of the topic
    if topic.endswith("temperature"):
        if RED_IS_ON:
            if value > MIN_TEMP or value < MAX_TEMP:
                res = Alert.RED_OFF.value
                RED_IS_ON = False
                publish(client, response_topic, res, 1)
                # TODO put it in a database and associate it with the client_id
        elif value <= MIN_TEMP or value >= MAX_TEMP:
            res = Alert.RED_ON.value
            RED_IS_ON = True
            publish(client, response_topic, res, 1)
            # TODO: send message to bot

    elif topic.endswith("light"):
        if value <= MIN_LIGHT:
            # TODO: send message to bot
            return
        return

    elif topic.endswith("humidity"):
        if value < MIN_HUMIDITY:
            # TODO: send message to bot
            return
        return

    elif topic.endswith("water"):
        # if the alert was already turned on
        if BLUE_IS_ON:
            if value:
                res = Alert.BLUE_OFF.value
                BLUE_IS_ON = False
                publish(client, response_topic, res, 1)
                # TODO put it in a database and associate it with the client_id
        elif not value:
            res = Alert.BLUE_ON.value
            BLUE_IS_ON = True
            publish(client, response_topic, res, 1)
            # TODO: send message to bot
    else:
        return

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


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
