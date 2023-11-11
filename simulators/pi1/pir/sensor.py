import time

import RPi.GPIO as GPIO
import keyboard


def run_pir_loop(device_id, callback, stop_event, pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)

    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda cb: callback(device_id))

    while not stop_event.is_set():
        time.sleep(0.1)