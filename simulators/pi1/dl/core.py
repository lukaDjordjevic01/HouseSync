import keyboard
import time
import RPi.GPIO as GPIO


def run(device_id, settings):
    print("Turn the light on with 'a', turn it of with 'd', exit with x: ")

    exit_flag = [False]

    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            exit_flag[0] = True
        elif e.name == 'a' and e.event_type == keyboard.KEY_DOWN:
            light_switch(True, device_id, settings['pin'])
        elif e.name == 'd' and e.event_type == keyboard.KEY_DOWN:
            light_switch(False, device_id, settings['pin'])

    keyboard.hook(on_key_event)

    while not exit_flag[0]:
        time.sleep(0.1)

    GPIO.cleanup()


def light_switch(switch, device_id, pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    if switch:
        GPIO.output(pin, GPIO.HIGH)
        print(device_id + " is on.")
        return
    GPIO.output(pin, GPIO.LOW)
    print(device_id + " is off.")
