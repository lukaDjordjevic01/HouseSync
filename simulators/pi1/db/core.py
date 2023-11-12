# import RPi.GPIO as GPIO
import time
import keyboard


def run(device_id, settings):
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)
    print("Buzz the buzzer with 'b' and exit this simulation with 'x'")
    exit_flag = [False]

    def on_key_event(e):
        if e.name == 'x' and e.event_type == keyboard.KEY_DOWN:
            exit_flag[0] = True
        elif e.name == 'b' and e.event_type == keyboard.KEY_DOWN:
            buzz(device_id, settings['pin'])

    keyboard.hook(on_key_event)

    while not exit_flag[0]:
        time.sleep(0.1)

    keyboard.unhook_all()
    #GPIO.cleanup()


def buzz(device_id, pin, pitch=440, duration=1):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        # GPIO.output(pin, True)
        time.sleep(delay)
        # GPIO.output(pin, False)
        time.sleep(delay)
    print(f"{device_id} buzzed")
    time.sleep(1)
