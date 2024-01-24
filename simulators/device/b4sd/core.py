import json
import threading
import time

from paho.mqtt import publish

from  ...communication_credentials import *
import paho.mqtt.client as mqtt

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}

alarm_clock_is_on = False


def on_connect(client, userdata, flags, rc):
    client.subscribe("alarm-clock")


def set_up_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: process_message(msg)

    mqtt_client.connect(host=mqtt_host, port=mqtt_port, keepalive=1000)
    mqtt_client.loop_start()


def process_message(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == "alarm-clock":
        global alarm_clock_is_on
        alarm_clock_is_on = payload['is_on']


def run_b4sd_thread(device_id, settings, stop_event):
    global alarm_clock_is_on
    if not settings["simulated"]:
        import RPi.GPIO as GPIO
        for segment in settings["segments"]:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        for digit in settings["digits"]:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    while not stop_event.is_set():
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)
        if not settings["simulated"]:
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(settings["segments"][loop], num[s[digit]][loop])
                    # if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    #     GPIO.output(25, 1)
                    # else:
                    #     GPIO.output(25, 0)
                GPIO.output(settings["digits"][digit], 0)
                time.sleep(0.001)
                GPIO.output(settings["digits"][digit], 1)

            if alarm_clock_is_on:
                time.sleep(0.5)
        else:
            print(s)
            time.sleep(2)
        publish.single("B4SD", json.dumps({"time": f"{s[0]}{s[1]}:{s[2]}{s[3]}"}), hostname=mqtt_host, port=mqtt_port)

    if settings["simulated"]:
        import RPi.GPIO as GPIO
        GPIO.cleanup()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting rgb simulator")
    b4sd_thread = threading.Thread(target=run_b4sd_thread,
                                   args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    b4sd_thread.start()
    if not all_sensors:
        b4sd_thread.join()
