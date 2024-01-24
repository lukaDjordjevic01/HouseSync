import json
import threading

from datetime import datetime
import time

from paho.mqtt import publish
from ...communication_credentials import *

Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd,
           0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5,
           0x300ff52ad]  # HEX code list
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]  # String list in same order as HEX list

ButtonsCommands = {"1": "white", "2": "red", "3": "green", "4": "blue", "5": "yellow", "6": "purple", "7": "lightBlue",
                   "OK": "on_off"}


def get_binary(pin, GPIO):
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The binary value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = GPIO.input(pin)  # The current value

    # Waits for the sensor to pull pin low
    while value:
        time.sleep(0.0001)  # This sleep decreases CPU utilization immensely
        value = GPIO.input(pin)

    # Records start time
    startTime = datetime.now()

    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            command.append((previousValue, pulseTime.microseconds))  # Store recorded data

        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0

        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)

    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])

    return binary


# Convert value to hex
def convert_hex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)  # Temporarely propper base 2
    return hex(tmpB2)


def run_ir_receiver_thread(device_id, settings, stop_event):
    if not settings['simulated']:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(settings["pin"], GPIO.IN)

    while not stop_event.is_set():
        if not settings['simulated']:
            inData = convert_hex(get_binary(settings["pin"], GPIO))  # Runs subs to get incoming hex value
            for button in range(len(Buttons)):  # Runs through every value in list
                if hex(Buttons[button]) == inData:  # Checks this against incoming
                    if ButtonsNames[button] in ButtonsCommands:
                        publish.single(topic="rgb-control",
                                       payload=json.dumps({"command": ButtonsCommands[ButtonsNames[button]]}),
                                       hostname=mqtt_host,
                                       port=mqtt_port)
        else:
            time.sleep(5)


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting ir_receiver simulator")
    ir_receiver_thread = threading.Thread(target=run_ir_receiver_thread,
                                          args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    ir_receiver_thread.start()
    if not all_sensors:
        ir_receiver_thread.join()
