import time
import random


import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json

from ...communication_credentials import *

DOORS_LOCKED = {"DS1": True, "DS2": True}


def on_connect(client, userdata, flags, rc):
    client.subscribe("DS")


def set_up_mqtt(device_id, callback, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(msg, device_id, callback,
                                                                        settings)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(msg, device_id, callback, settings):
    payload = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == "DS":
        if payload["device_id"] == device_id:
            DOORS_LOCKED[device_id] = not DOORS_LOCKED[device_id]
            callback(device_id, DOORS_LOCKED[device_id], settings)


def run_ds_simulator(device_id, callback, stop_event, settings):
    set_up_mqtt(device_id, callback, settings)
    while not stop_event.is_set():
        time.sleep(2)
