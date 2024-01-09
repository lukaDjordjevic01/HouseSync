# import RPi.GPIO as GPIO
import json
import threading
import time

import paho.mqtt.client as mqtt
from paho.mqtt import publish

from ...communication_credentials import *

alarm_is_on = False


def on_connect(client, userdata, flags, rc):
    client.subscribe("Alarm")


def set_up_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(msg)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == "Alarm":
        global alarm_is_on
        if payload['command'] == 'on':
            alarm_is_on = True
        elif payload['command'] == 'off':
            alarm_is_on = False


def run_db_thread(device_id, settings, stop_event):
    set_up_mqtt()
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)

    while not stop_event.is_set():
        buzz(device_id, settings['pin'])
        time.sleep(0.1)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting db simulator")
    db_thread = threading.Thread(target=run_db_thread,
                                 args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    db_thread.start()
    if not all_sensors:
        db_thread.join()


def buzz(device_id, pin, pitch=440):
    period = 1.0 / pitch
    delay = period / 2
    while alarm_is_on:
        # GPIO.output(pin, True)
        time.sleep(delay)
        # GPIO.output(pin, False)
        time.sleep(delay)
        publish.single("Alarm", json.dumps({
            'command': 'notify',
            "message": f"{device_id} buzzed",
            "device_id": device_id
        }))
        print(f"{device_id} buzzed")
        time.sleep(2)
