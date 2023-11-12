import RPi.GPIO as GPIO
import time

import keyboard


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


def read_line(line, characters, settings, callback):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(settings['C1']) == 1:
        callback(characters[0])
    if GPIO.input(settings['C2']) == 1:
        callback(characters[1])
    if GPIO.input(settings['C3']) == 1:
        callback(characters[2])
    if GPIO.input(settings['C4']) == 1:
        callback(characters[3])
    GPIO.output(line, GPIO.LOW)


def run_dms_loop(device_id, callback, stop_event, settings):
    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    print(device_id + " loop started.")
    setup(settings)

    while True:
        read_line(settings['R1'], ["1", "2", "3", "A"], settings, callback)
        read_line(settings['R2'], ["4", "5", "6", "B"], settings, callback)
        read_line(settings['R3'], ["7", "8", "9", "C"], settings, callback)
        read_line(settings['R4'], ["*", "0", "#", "D"], settings, callback)
        time.sleep(0.2)
