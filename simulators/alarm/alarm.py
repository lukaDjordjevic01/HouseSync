import json

from paho.mqtt import publish
from ..communication_credentials import *


def turn_on_alarm(device_id):
    payload = {
        "device_id": device_id,
        "command": "on"
    }
    publish.single("Alarm", json.dumps(payload), hostname=mqtt_host, port=mqtt_port)


def turn_off_alarm(device_id):
    payload = {
        "device_id": device_id,
        "command": "off"
    }
    publish.single("Alarm", json.dumps(payload), hostname=mqtt_host, port=mqtt_port)
