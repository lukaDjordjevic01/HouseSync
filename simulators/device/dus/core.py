import threading
import time
import json
from ...communication_credentials import *


from paho.mqtt import publish

from .simulator import run_dus_simulator

dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()

        publish.multiple(local_dht_batch, hostname=mqtt_host, port=mqtt_port)
        print(f'published {publish_data_limit} dus values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, distance, publish_event, settings):
    global publish_data_counter, publish_data_limit

    if distance is not None:
        distance_payload = {
            "measurement": "Distance(cm)",
            "id": device_id,
            "simulated": settings['simulated'],
            "runs_on": settings["runs_on"],
            "name": settings["name"],
            "value": distance
        }

        publish.single("DUS", json.dumps(distance_payload), hostname=mqtt_host, port=mqtt_port)

        with counter_lock:
            dus_batch.append(('Distance', json.dumps(distance_payload), 0, True))
            publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()
    else:
        print(f"Measurement on {device_id} timed out")


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print(f"Starting {device_id} simulator")
        dus_thread = threading.Thread(target=run_dus_simulator, args=(device_id, 2, callback, stop_event,
                                                                      publish_event, settings))
        dus_thread.start()
        if not all_sensors:
            dus_thread.join()
    else:
        from .sensor import run_dus_loop, DUS
        print(f"Starting {device_id} loop")
        dus = DUS(settings['trig_pin'], settings['echo_pin'])
        dus_thread = threading.Thread(target=run_dus_loop, args=(dus, device_id, callback, stop_event,
                                                                 publish_event, settings))
        dus_thread.start()
        if not all_sensors:
            dus_thread.join()
