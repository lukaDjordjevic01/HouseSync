import json
import threading

from paho.mqtt import publish

from .simulator import run_gsg_simulator


gsg_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, gsg_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gsg_batch = gsg_batch.copy()
            publish_data_counter = 0
            gsg_batch.clear()
        publish.multiple(local_gsg_batch, hostname="localhost", port=1883)
        print(f'published {publish_data_limit} dht values')
        for item in local_gsg_batch:
            print(item)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gsg_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, acceleration, rotation, publish_event, settings):
    global publish_data_counter, publish_data_limit

    acceleration = [round(value, 4) for value in acceleration]
    rotation = [round(value, 4) for value in rotation]

    acceleration_payload = {
        "measurement": "Acceleration",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": ' '.join(map(str, acceleration))
    }

    rotation_payload = {
        "measurement": "Rotation",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": ' '.join(map(str, rotation))
    }

    #ako se detektuje znacajan pomeraj onda aktivirati alarm

    with counter_lock:
        gsg_batch.append(('Acceleration', json.dumps(acceleration_payload), 0, True))
        gsg_batch.append(('Rotation', json.dumps(rotation_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    if settings['simulated']:
        print("Starting gsg sumilator")
        gsg_thread = threading.Thread(target=run_gsg_simulator,
                                      args=(device_id, 2, callback, stop_event, publish_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        gsg_thread.start()
        if not all_sensors:
            gsg_thread.join()
    else:
        from .sensor import run_gsg_loop
        print(f"Starting {device_id} loop")
        gsg_thread = threading.Thread(target=run_gsg_loop,
                                      args=(device_id, 2, callback, stop_event, publish_event, settings))
        gsg_thread.start()
        if not all_sensors:
            gsg_thread.join()
