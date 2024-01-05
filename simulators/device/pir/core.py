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

    #kada detektuje pokret salje svom dus-u signal on zabelezi udaljenost
    #ako je dpir1 onda ukljuci i DL1
    #videti dal neko ulazi il izlazi
    #brojno stanje osoba u objektu -> globalna promenljiva
    # ako je neki od RPIR-ova a nema osoba u objektu, ukljucuhe se alarm

    with counter_lock:
        pir_batch.append(('Movement', json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print(f"Starting {device_id} simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(device_id, callback, stop_event, publish_event,
                                                                      settings))
        pir_thread.start()
        if not all_sensors:
            pir_thread.join()
    else:
        from .sensor import run_pir_loop
        print(f"Starting {device_id} loop")
        pir_thread = threading.Thread(target=run_pir_loop, args=(device_id, callback, stop_event, publish_event,
                                                                 settings))
        pir_thread.start()
        if not all_sensors:
            pir_thread.join()
