import json
import threading
import time

import paho.mqtt.client as mqtt
from paho.mqtt import publish
from .Adafruit_LCD1602 import Adafruit_CharLCD
from ...communication_credentials import *


gdht_temp = 0
gdht_humidity = 0

lcd_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")


def set_up_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(json.loads(msg.payload.decode('utf-8')))

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(data):
    if data['id'] != 'GDHT':
        return

    if data['measurement'] == 'Temperature':
        global gdht_temp
        gdht_temp = data['value']
    elif data['measurement'] == 'Humidity':
        global gdht_humidity
        gdht_humidity = data['value']


def publisher_task(event, lcd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_lcd_batch = lcd_batch.copy()
            publish_data_counter = 0
            lcd_batch.clear()
        publish.multiple(local_lcd_batch, hostname=mqtt_host, port=mqtt_port)
        print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, lcd_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def callback(device_id, display_data, publish_event, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "Garage LCD",
        "id": device_id,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": display_data
    }

    publish.single("GLCD", payload=json.dumps({"display_data": display_data}), hostname=mqtt_host, port=mqtt_port)


def run_lcd_thread(device_id, delay, settings, stop_event):
    global gdht_temp, gdht_humidity
    set_up_mqtt()
    while not stop_event.is_set():
        message = f"  Temperature: {gdht_temp}C\n  Humidity: {gdht_humidity}%\n"
        if not settings['simulated']:
            lcd = Adafruit_CharLCD(settings['pin_rs'], settings['pin_e'], settings['pins_db'])
            lcd.clear()
            lcd.message(message)
        callback(device_id, message, publish_event, settings)
        time.sleep(delay)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting lcd sumilator")
    lcd_thread = threading.Thread(target=run_lcd_thread,
                                  args=(device_id, 2, settings, stop_event))
    threads[device_id] = stop_event
    lcd_thread.start()
    if not all_sensors:
        lcd_thread.join()
