import threading
import time
import json

from paho.mqtt import publish
from .simulator import run_pir_simulator
import paho.mqtt.client as mqtt
from ...communication_credentials import *

pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

dus_last_values = {}
dus_current_values = {'DUS1': 0, 'DUS2': 0}


def on_connect(client, userdata, flags, rc):
    client.subscribe("DUS")


def set_up_mqtt(device_id):
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(device_id,
                                                                           json.loads(msg.payload.decode('utf-8')))

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(device_id, data):
    if device_id == "DPIR1" and data['id'] == 'DUS1' or device_id == "DPIR2" and data['id'] == 'DUS2':
        dus_last_values[data['id']] = dus_current_values[data['id']]
        dus_current_values[data['id']] = data['value']


def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()

        publish.multiple(local_dht_batch, hostname=mqtt_host, port=mqtt_port)
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

    if device_id == "DPIR1":
        publish.single("DL",
                       hostname=mqtt_host,
                       port=mqtt_port)
        publish.single("DPIR",
                       json.dumps({"device_id": device_id,
                                   "distance_diff": dus_current_values['DUS1'] - dus_last_values['DUS1']}),
                       hostname=mqtt_host,
                       port=mqtt_port)
    if device_id == "DPIR2":
        publish.single("DPIR",
                       json.dumps({"device_id": device_id,
                                   "distance_diff": dus_current_values['DUS2'] - dus_last_values['DUS2']}),
                       hostname=mqtt_host,
                       port=mqtt_port)
    if "RPIR" in device_id:
        publish.single("RPIR",
                       json.dumps({"device_id": device_id}),
                       hostname=mqtt_host,
                       port=mqtt_port)
    if device_id == "BIR":
        publish.single(topic="rgb-control",
                       payload=json.dumps({"command": "on_off"}),
                       hostname=mqtt_host,
                       port=mqtt_port)

    with counter_lock:
        pir_batch.append(('Movement', json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    set_up_mqtt(device_id)
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
