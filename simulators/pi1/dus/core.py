import threading
import time

from .simulator import run_dus_simulator


def callback(device_id, distance):
    if distance is not None:
        print(f"{device_id} recorded someone at the distance of {distance}cm")
    else:
        print(f"Measurement on {device_id} timed out")


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print(f"Starting {device_id} simulator")
        dus_thread = threading.Thread(target=run_dus_simulator, args=(device_id, 2, callback, stop_event))
        dus_thread.start()
        dus_thread.join()
    else:
        from .sensor import run_dus_loop, DUS
        print(f"Starting {device_id} loop")
        dus = DUS(settings['trig_pin'], settings['echo_pin'])
        pir_thread = threading.Thread(target=run_dus_loop, args=(dus, device_id, callback, stop_event))
        pir_thread.start()
        pir_thread.join()