import time
import random

import keyboard


def run_pir_simulator(device_id, callback, stop_event, publish_event, settings):
    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    while True:
        time.sleep(random.randint(1, 8))
        callback(device_id, publish_event, settings)
        if stop_event.is_set():
            break
