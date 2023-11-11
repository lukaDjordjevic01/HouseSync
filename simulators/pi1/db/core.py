#import RPi.GPIO as GPIO
import time


def run(device_id, settings):
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)
    while True:
        option = input("Buzz the buzzer with 'b' and exit this simulation with 'x': ")
        if option == 'b':
            buzz(device_id, settings['pin'])
        else:
            return


def buzz(device_id, pin, pitch=440, duration=1):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        #GPIO.output(pin, True)
        time.sleep(delay)
        #GPIO.output(pin, False)
        time.sleep(delay)
    print(f"{device_id} buzzed")
    time.sleep(1)