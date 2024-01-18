import time
import random


def generate_values(initial_distance=9):
    distance = initial_distance
    while True:
        distance = distance + random.randint(-2, 2)
        if distance < 0:
            distance = 9
        yield distance


def run_dus_simulator(device_id, delay, callback, stop_event, publish_event, settings):

    for distance in generate_values():
        time.sleep(delay)
        callback(device_id, distance, publish_event, settings)
        if stop_event.is_set():
            break
