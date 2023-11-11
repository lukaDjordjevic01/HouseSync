import threading
import time

from .simulator import run_pir_simulator


def callback(device_id):
    print(f"Someone passed past the {device_id}")


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print(f"Starting {device_id} simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(device_id, callback, stop_event))
        pir_thread.start()
        pir_thread.join()
    else:
        from .sensor import run_pir_loop
        print(f"Starting {device_id} loop")
        pir_thread = threading.Thread(target=run_pir_loop, args=(device_id, callback, stop_event, settings['pin']))
        pir_thread.start()
        pir_thread.join()