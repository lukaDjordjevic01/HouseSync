import RPi.GPIO as GPIO
import time

import keyboard

pin = ""

def setup(settings):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(settings['R1'], GPIO.OUT)
    GPIO.setup(settings['R2'], GPIO.OUT)
    GPIO.setup(settings['R3'], GPIO.OUT)
    GPIO.setup(settings['R4'], GPIO.OUT)

    GPIO.setup(settings['C1'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(settings['C2'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(settings['C3'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(settings['C4'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def read_line(line, characters, settings, callback, device_id, publish_event):
    global pin
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(settings['C1']) == 1:
        pin += characters[0]
    if GPIO.input(settings['C2']) == 1:
        pin += characters[1]
    if GPIO.input(settings['C3']) == 1:
        pin += characters[2]
        if characters[2] == "#":
            callback(device_id, pin, publish_event, settings)
            pin = ""
    if GPIO.input(settings['C4']) == 1:
        pin += characters[3]
    GPIO.output(line, GPIO.LOW)


def run_dms_loop(device_id, callback, stop_event, publish_event, settings):

    print(device_id + " loop started.")
    setup(settings)

    while not stop_event.is_set():
        read_line(settings['R1'], ["1", "2", "3", "A"], settings, callback, device_id, publish_event)
        read_line(settings['R2'], ["4", "5", "6", "B"], settings, callback, device_id, publish_event)
        read_line(settings['R3'], ["7", "8", "9", "C"], settings, callback, device_id, publish_event)
        read_line(settings['R4'], ["*", "0", "#", "D"], settings, callback, device_id, publish_event)
        time.sleep(0.2)
