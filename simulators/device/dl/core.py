import json
import threading

import time
import paho.mqtt.client as mqtt
from ...communication_credentials import *


# import RPi.GPIO as GPIO


def on_connect(client, userdata, flags, rc):
    client.subscribe("DL")


def set_up_mqtt(device_id, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(device_id, settings)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(device_id, settings):
    light_switch(True, device_id, settings['pin'])
    time.sleep(10)
    light_switch(False, device_id, settings['pin'])


def run_dl_thread(device_id, settings, stop_event):
    set_up_mqtt(device_id, settings)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pin, GPIO.OUT)
    while not stop_event.is_set():
        time.sleep(0.1)
    # GPIO.cleanup()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting dl simulator")
    dl_thread = threading.Thread(target=run_dl_thread,
                                 args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    dl_thread.start()
    if not all_sensors:
        dl_thread.join()


def light_switch(switch, device_id, pin):
    if switch:
        # GPIO.output(pin, GPIO.HIGH)
        print(device_id + " is on.")
        return
    # GPIO.output(pin, GPIO.LOW)
    print(device_id + " is off.")
