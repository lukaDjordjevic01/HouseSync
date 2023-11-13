import threading
import time

from .simulator import run_dht_simulator


def callback(humidity, temperature, code=''):
    t = time.localtime()
    print("= " * 20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run(device_id, threads, settings, stop_event):
    if settings['simulated']:
        print("Starting dht sumilator")
        dht_thread = threading.Thread(target=run_dht_simulator, args=(2, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dht_thread.start()
        dht_thread.join()
    else:
        from sensor import run_dht_loop, DHT
        print("Starting dht loop")
        dht = DHT(settings['pin'])
        dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, callback, stop_event))
        threads[device_id] = stop_event
        print(device_id + " sumilator started")
        dht_thread.start()
        dht_thread.join()

