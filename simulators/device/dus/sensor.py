import RPi.GPIO as GPIO
import time


class DUS(object):
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iteration = 0
        while GPIO.input(self.echo_pin) == 0:
            if iteration > max_iter:
                return None
            pulse_start_time = time.time()
            iteration += 1

        iteration = 0
        while GPIO.input(self.echo_pin) == 1:
            if iteration > max_iter:
                return None
            pulse_end_time = time.time()
            iteration += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2
        return distance


def run_dus_loop(dus, device_id, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        distance = dus.get_distance()
        callback(device_id, distance, publish_event, settings)
        if stop_event.is_set():
            break

    GPIO.cleanup()
