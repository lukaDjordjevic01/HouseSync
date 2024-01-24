import json
import threading

from paho.mqtt import publish

from .simulator import run_dms_simulator
from ...communication_credentials import *


def callback(device_id, pin, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "Passwords",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": pin
    }

    publish.single("Passwords", json.dumps(payload), hostname=mqtt_host, port=mqtt_port)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print("Starting dms sumilator")
        dms_thread = threading.Thread(target=run_dms_simulator,
                                      args=(device_id, 2, callback, stop_event, settings))
        threads[device_id] = stop_event
        dms_thread.start()
        if not all_sensors:
            dms_thread.join()
    else:
        from .sensor import run_dms_loop
        print("Starting dms loop")
        dms_thread = threading.Thread(target=run_dms_loop,
                                      args=(device_id, callback, stop_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dms_thread.start()
        if not all_sensors:
            dms_thread.join()
