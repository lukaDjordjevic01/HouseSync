import math
import time
import paho.mqtt.client as mqtt
from ...communication_credentials import *


is_significant = False


def on_connect(client, userdata, flags, rc):
    client.subscribe("GSG-scenario")


def set_up_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message()

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message():
    global is_significant
    is_significant = True


def run_gsg_simulator(device_id, delay, callback, stop_event, publish_event, settings):
    global is_significant
    set_up_mqtt()
    time_step = 0.1  # Time step for simulation
    time_elapsed = 0.0  # Initialize time elapsed

    while not stop_event.is_set():
        # Simulate acceleration values (sine function for periodic motion)
        accel_x = 0.5 * math.sin(2 * math.pi * time_elapsed)
        accel_y = 0.7 * math.sin(1.5 * math.pi * time_elapsed)
        accel_z = 0.3 * math.sin(math.pi * time_elapsed)

        if is_significant:
            accel_x = 5
            accel_y = 5
            accel_z = 5
            is_significant = False

        # Simulate rotation values (cosine function for periodic motion)
        gyro_x = 50.0 * math.cos(2 * math.pi * time_elapsed)
        gyro_y = 30.0 * math.cos(1.5 * math.pi * time_elapsed)
        gyro_z = 20.0 * math.cos(math.pi * time_elapsed)

        acceleration = [accel_x, accel_y, accel_z]
        rotation = [gyro_x, gyro_y, gyro_z]

        callback(device_id, acceleration, rotation, publish_event, settings)
        time.sleep(delay)

        time_elapsed += time_step
