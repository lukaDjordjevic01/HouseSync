import threading
import time
import json

from paho.mqtt import publish
from .simulator import run_pir_simulator

pir_batch = []
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

        print(local_dht_batch)
        publish.multiple(local_dht_batch, hostname="localhost", port=1883)
        print(f'published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, publish_event, settings):
    global publish_data_counter, publish_data_limit

    movement_payload = {
        "measurement": "Movement detection",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "Person passed"
    }

    with counter_lock:
        pir_batch.append(('Movement', json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print(f"Starting {device_id} simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(device_id, callback, stop_event, publish_event,
                                                                      settings))
        pir_thread.start()
        #pir_thread.join()
    else:
        from .sensor import run_pir_loop
        print(f"Starting {device_id} loop")
        pir_thread = threading.Thread(target=run_pir_loop, args=(device_id, callback, stop_event, publish_event,
                                                                 settings))
        pir_thread.start()
        pir_thread.join()
