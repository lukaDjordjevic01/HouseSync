import json
import time
import paho.mqtt.client as mqtt

from paho.mqtt import publish

from ...communication_credentials import *


def on_connect(client, userdata, flags, rc):
    client.subscribe("DPIR-scenario")
    client.subscribe("RPIR-scenario")


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
    if device_id != payload['device_id']:
        return
    callback(device_id, publish_event, settings)


def run_pir_simulator(device_id, callback, stop_event, publish_event, settings):
    set_up_mqtt(device_id, callback, publish_event, settings)
    while True:
        time.sleep(0.1)
