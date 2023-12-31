import time
import random

import keyboard


def generate_values():
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#']

    while True:
        yield random.choice(characters)


def run_dms_simulator(delay, callback, stop_event):
    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    for o in generate_values():
        time.sleep(delay)
        callback(o)
        if stop_event.is_set():
            break
