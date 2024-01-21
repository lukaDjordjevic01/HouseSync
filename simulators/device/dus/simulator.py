import json
import time
import random

from paho.mqtt import publish

from ...communication_credentials import *
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe("DUS-scenario")


def set_up_mqtt(device_id, callback, publish_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(device_id,
                                                                           msg,
                                                                           callback,
                                                                           publish_event,
                                                                           settings)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(device_id, msg, callback, publish_event, settings):
    payload = json.loads(msg.payload.decode('utf-8'))
    if device_id != payload["device_id"]:
        return

    dpir_id = "DPIR1" if device_id == "DUS1" else "DPIR2"
    if payload["scenario"] == "in":
        callback(payload['device_id'], 20.0, publish_event, settings)
        time.sleep(0.5)
        callback(payload['device_id'], 10.0, publish_event, settings)
        time.sleep(0.5)
        publish.single("DPIR-scenario", json.dumps({"device_id": dpir_id}))
    elif payload["scenario"] == "out":
        callback(payload['device_id'], 10.0, publish_event, settings)
        time.sleep(0.5)
        callback(payload['device_id'], 20.0, publish_event, settings)
        time.sleep(0.5)
        publish.single("DPIR-scenario", json.dumps({"device_id": dpir_id}))


def generate_values(initial_distance=9.0):
    distance = initial_distance
    while True:
        distance = distance + random.randint(-2, 2)
        if distance < 0:
            distance = 9
        yield float(distance)


def run_dus_simulator(device_id, delay, callback, stop_event, publish_event, settings):
    set_up_mqtt(device_id, callback, publish_event, settings)
    while not stop_event.is_set():
        time.sleep(0.1)
