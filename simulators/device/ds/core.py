import json
import threading

from paho.mqtt import publish

from .simulator import run_ds_simulator
from ...communication_credentials import *


def callback(device_id, locked, settings):
    global publish_ds_data_counter, publish_ds_data_limit

    payload = {
        "measurement": "Door locked",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": locked
    }

    publish.single("Door", json.dumps(payload), hostname=mqtt_host, port=mqtt_port)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print("Starting ds sumilator")
        ds_thread = threading.Thread(target=run_ds_simulator,
                                     args=(device_id, callback, stop_event, settings))
        threads[device_id] = stop_event
        ds_thread.start()
        if not all_sensors:
            ds_thread.join()
    else:
        from .sensor import run_ds_loop
        print("Starting dms loop")
        ds_thread = threading.Thread(target=run_ds_loop,
                                      args=(device_id, callback, stop_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        ds_thread.start()
        if not all_sensors:
            ds_thread.join()
