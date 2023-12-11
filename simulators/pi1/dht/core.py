import json
import threading
import time

from paho.mqtt import publish

from .simulator import run_dht_simulator

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname="localhost", port=1883)
        print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, humidity, temperature, publish_event, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("=" * 20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Device id: {device_id}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print("Starting dht sumilator")
        dht_thread = threading.Thread(target=run_dht_simulator,
                                      args=(device_id, 2, callback, stop_event, publish_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dht_thread.start()
        dht_thread.join()
    else:
        from sensor import run_dht_loop, DHT
        print("Starting dht loop")
        dht = DHT(settings['pin'])
        dht_thread = threading.Thread(target=run_dht_loop,
                                      args=(device_id, dht, 2, callback, stop_event, publish_event, settings))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dht_thread.start()
        dht_thread.join()
