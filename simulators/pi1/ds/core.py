import threading
from .simulator import run_ds_simulator


def callback(device_id, locked):
    if locked:
        print(device_id + " is locked.")
        return
    print(device_id + " is unlocked.")


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print("Starting ds sumilator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(device_id, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        ds_thread.start()
        ds_thread.join()
    else:
        from .sensor import run_dms_loop
        print("Starting dms loop")
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dms_thread.start()
        dms_thread.join()
