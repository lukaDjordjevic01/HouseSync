import json
import threading
import time

import paho.mqtt.client as mqtt
from paho.mqtt import publish

from ...communication_credentials import *


def on_connect(client, userdata, flags, rc):
    client.subscribe("BRGB")


def set_up_mqtt(device_id, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(msg, device_id, settings)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(msg, device_id, settings):
    payload = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == device_id:
        process_command(settings, payload['command'])


def run_rgb_thread(device_id, settings, stop_event):
    set_up_mqtt(device_id, settings)
    if not settings["simulated"]:
        import RPi.GPIO as GPIO
        # set pins as outputs
        GPIO.setup(settings["red_ping"], GPIO.OUT)
        GPIO.setup(settings["green_pin"], GPIO.OUT)
        GPIO.setup(settings["blues_pin"], GPIO.OUT)

    while not stop_event.is_set():

        time.sleep(2)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting rgb simulator")
    rgb_thread = threading.Thread(target=run_rgb_thread,
                                  args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    rgb_thread.start()
    if not all_sensors:
        rgb_thread.join()


def process_command(settings, command):
    if not settings["simulated"]:
        from sensor import change_color
        change_color[command](settings)
    do_something[command]("aaaaaaaaaaaa")


# rename later while working on it
do_something = {
    'off': print
}
