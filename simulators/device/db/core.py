# import RPi.GPIO as GPIO
import json
import threading
import time

import paho.mqtt.client as mqtt
from paho.mqtt import publish

from ...communication_credentials import *

alarm_is_on = False

alarm_clock_is_on = False


def on_connect(client, userdata, flags, rc):
    client.subscribe("Alarm")
    client.subscribe("alarm-clock")


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
    elif msg.topic == "alarm-clock":
        global alarm_clock_is_on
        alarm_clock_is_on = payload['is_on']


def run_db_thread(device_id, settings, stop_event):
    set_up_mqtt()
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)

    while not stop_event.is_set():
        buzz_loop(device_id, settings['pin'])
        time.sleep(0.1)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting db simulator")
    db_thread = threading.Thread(target=run_db_thread,
                                 args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    db_thread.start()
    if not all_sensors:
        db_thread.join()


def buzz_loop(device_id, pin, pitch=440):
    period = 1.0 / pitch
    delay = period / 2
    if device_id == "BB":
        while alarm_is_on or alarm_clock_is_on:
            buzz(device_id, pin, delay)
    else:
        while alarm_is_on:
            buzz(device_id, pin, delay)


def buzz(device_id, pin, delay):
    # GPIO.output(pin, True)
    time.sleep(delay)
    # GPIO.output(pin, False)
    time.sleep(delay)
    print(f"{device_id} buzzed")

    if device_id == "DB":
        payload = {
            "message": "Security alarm is triggered.",
            "command": "notify"
        }
        publish.single("Alarm", json.dumps(payload), hostname=mqtt_host, port=mqtt_port)

    time.sleep(2)
