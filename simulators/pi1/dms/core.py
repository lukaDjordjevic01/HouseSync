import threading

from .simulator import run_dms_simulator


def callback(output):
    print(f"Pressed: {output}")


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print("Starting dms sumilator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dms_thread.start()
        dms_thread.join()
    else:
        from .sensor import run_dms_loop
        print("Starting dms loop")
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dms_thread.start()
        dms_thread.join()
