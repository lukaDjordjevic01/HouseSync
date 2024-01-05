import json
import threading

from paho.mqtt import publish

from .simulator import run_ds_simulator

ds_batch = []
publish_ds_data_counter = 0
publish_ds_data_limit = 5
ds_counter_lock = threading.Lock()


def publisher_task(event, batch):
    global publish_ds_data_counter, publish_ds_data_limit
    while True:
        event.wait()
        with ds_counter_lock:
            local_batch = batch.copy()
            publish_ds_data_counter = 0
            batch.clear()
        publish.multiple(local_batch, hostname="localhost", port=1883)
        print(f'published {publish_ds_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, locked, publish_event, settings):
    global publish_ds_data_counter, publish_ds_data_limit

    payload = {
        "measurement": "Door locked",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": locked
    }

    #meriti vreme od prethodnog callbacka i onda ukljuciti alarm ako treba
    # ako se ukljucio alarm, kad stigner signal za zakljucavanje iskljuciti alarm

    with ds_counter_lock:
        ds_batch.append(('Door', json.dumps(payload), 0, True))
        publish_ds_data_counter += 1

    if publish_ds_data_counter >= publish_ds_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print("Starting ds sumilator")
        ds_thread = threading.Thread(target=run_ds_simulator,
                                     args=(device_id, callback, stop_event, publish_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        ds_thread.start()
        if not all_sensors:
            ds_thread.join()
    else:
        from .sensor import run_ds_loop
        print("Starting dms loop")
        ds_thread = threading.Thread(target=run_ds_loop,
                                      args=(device_id, callback, stop_event, publish_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        ds_thread.start()
        if not all_sensors:
            ds_thread.join()
