import time
import random

import keyboard


def generate_values(initial_distance=9):
    distance = initial_distance
    while True:
        distance = distance + random.randint(-2, 2)
        if distance < 0:
            distance = 9
        yield distance


def run_dus_simulator(device_id, delay, callback, stop_event):
    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            stop_event.set()

    keyboard.hook(on_key_event)

    for distance in generate_values():
        time.sleep(delay)
        callback(device_id, distance)
        if stop_event.is_set():
            break
