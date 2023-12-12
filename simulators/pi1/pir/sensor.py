import time

import RPi.GPIO as GPIO
import keyboard


def run_pir_loop(device_id, callback, stop_event, publish_event, settings):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['pin'], GPIO.IN)

    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    GPIO.add_event_detect(settings['pin'], GPIO.RISING, callback=callback(device_id, publish_event, settings))

    while not stop_event.is_set():
        time.sleep(0.1)

    GPIO.cleanup()