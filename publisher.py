#
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
import ssl
from dotenv import load_dotenv
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish


load_dotenv()

hostname = os.environ['HOSTNAME']
username = os.environ['CLIENT_NAME']
password = os.environ['CLIENT_PASSWORD']

# create a set of 2 test messages that will be published at the same time
# msgs = [{'topic': "plant/temperature", 'payload': "20"}, ("plant/light", "5", 0, False)]

# use TLS for secure connection with HiveMQ Cloud
# sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)

# # put in your cluster credentials and hostname
# auth = {'username': username, 'password': password}
# publish.multiple(msgs, hostname=hostname,
#                     port=8883, auth=auth, tls=sslSettings, protocol=paho.MQTTv31)



def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="sensor_temp", clean_session=True, userdata=None, protocol=paho.MQTTv31)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(username, password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(hostname, 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of plant by using the wildcard "#"
client.subscribe("device/1/led", qos=1)

# client.publish("plant/temperature", "20", qos=0)
# client.publish("plant/temperature", "5", qos=0)
client.publish("device/1/dht", "H:50,T:200", qos=0)
client.loop_forever()

# auth = {'username': username, 'password': password}
# sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)
# msgs = [{'topic': "plant/temperature", 'payload': "20"}, ("plant/light", "5", 0, False)]
# publish.multiple(msgs, hostname=hostname,
#                     port=8883, auth=auth, tls=sslSettings, protocol=paho.MQTTv31)


# topic:            QOS:
# plant/temperature 0
# plant/light       0
# plant/humidity    0
# plant/water       0

# plant/led 1 :4
# comandi: "accendi led1, spegni led1, accendi led2, spegni led2"