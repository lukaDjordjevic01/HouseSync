import time
import random

import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json

from ...communication_credentials import *


def on_connect(client, userdata, flags, rc):
    client.subscribe("DMS")


def set_up_mqtt(device_id, callback, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(msg, device_id, callback,
                                                                           settings)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(msg, device_id, callback, settings):
    payload = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == "DMS":
        if payload["scenario"] == "correct":
            callback(device_id, "1234#", settings)
        elif payload["scenario"] == "incorrect":
            callback(device_id, "5678#", settings)


def generate_password(scenario):
    pass
    # password = ""
    # characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #
    # for i in range(4):
    #     password += random.choice(characters)
    #     if len(password) == 4:
    #         password += "#"
    #         return password


def run_dms_simulator(device_id, delay, callback, stop_event, settings):
    set_up_mqtt(device_id, callback, settings)
    while not stop_event.is_set():
        time.sleep(delay)
