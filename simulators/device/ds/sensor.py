import time

# import RPi.GPIO as GPIO


def run_ds_loop(device_id, callback, stop_event, pin, publish_event, settings):


    print(device_id + " loop started.")
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda x: callback(device_id, False, publish_event, settings), bouncetime=100)
    # GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda x: callback(device_id, True, publish_event, settings), bouncetime=100)

    while not stop_event.is_set():
        time.sleep(0.1)
