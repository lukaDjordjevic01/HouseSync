import time

# mozda poterati kao thread
def run(device_id, settings):
    if not settings["simulated"]:
        import RPi.GPIO as GPIO
        # set pins as outputs
        GPIO.setup(settings["red_ping"], GPIO.OUT)
        GPIO.setup(settings["green_pin"], GPIO.OUT)
        GPIO.setup(settings["blues_pin"], GPIO.OUT)

    while True:
        # slusaj neki dogadjaj
        command = 'off'

        if not settings["simulated"]:
            from sensor import change_color
            change_color[command](settings)

        do_something[command]("aaaaaaaaaaaa")
        time.sleep(2)


# rename later while working on it
do_something = {
    'off': print
}