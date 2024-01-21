import threading
import time

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}


def run_b4sd_thread(device_id, settings, stop_event):
    if not settings["simulated"]:
        import RPi.GPIO as GPIO
        for segment in settings["segments"]:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        for digit in settings["digits"]:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    while not stop_event.is_set():
        if not settings["simulated"]:
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            for digit in range(4):
                for loop in range(0, 7):
                    GPIO.output(settings["segments"][loop], num[s[digit]][loop])
                    if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                        GPIO.output(25, 1)
                    else:
                        GPIO.output(25, 0)
                GPIO.output(settings["digits"][digit], 0)
                time.sleep(0.001)
                GPIO.output(settings["digits"][digit], 1)
        else:
            print(time.ctime().format("hh:mm:ss"))
            time.sleep(2)

    if settings["simulated"]:
        import RPi.GPIO as GPIO
        GPIO.cleanup()


def run(device_id, threads, settings, stop_event, all_sensors=False):
    print("Starting rgb simulator")
    b4sd_thread = threading.Thread(target=run_b4sd_thread,
                                  args=(device_id, settings, stop_event))
    threads[device_id] = stop_event
    b4sd_thread.start()
    if not all_sensors:
        b4sd_thread.join()