import time
import random

import keyboard


def run_ds_simulator(device_id, callback, stop_event, publish_event, settings):
    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    locked = False
    while True:
        time.sleep(random.randint(1, 8))
        callback(device_id, locked, publish_event, settings)
        locked = not locked
        if stop_event.is_set():
            break
