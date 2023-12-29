import RPi.GPIO as GPIO


def turnOff(settings):
    GPIO.output(settings["red_pin"], GPIO.LOW)
    GPIO.output(settings["green_pin"], GPIO.LOW)
    GPIO.output(settings["blue_pin"], GPIO.LOW)


def white(settings):
    GPIO.output(settings["red_pin"], GPIO.HIGH)
    GPIO.output(settings["green_pin"], GPIO.HIGH)
    GPIO.output(settings["blue_pin"], GPIO.HIGH)


def red(settings):
    GPIO.output(settings["red_pin"], GPIO.HIGH)
    GPIO.output(settings["green_pin"], GPIO.LOW)
    GPIO.output(settings["blue_pin"], GPIO.LOW)


def green(settings):
    GPIO.output(settings["red_pin"], GPIO.LOW)
    GPIO.output(settings["green_pin"], GPIO.HIGH)
    GPIO.output(settings["blue_pin"], GPIO.LOW)


def blue(settings):
    GPIO.output(settings["red_pin"], GPIO.LOW)
    GPIO.output(settings["green_pin"], GPIO.LOW)
    GPIO.output(settings["blue_pin"], GPIO.HIGH)


def yellow(settings):
    GPIO.output(settings["red_pin"], GPIO.HIGH)
    GPIO.output(settings["green_pin"], GPIO.HIGH)
    GPIO.output(settings["blue_pin"], GPIO.LOW)


def purple(settings):
    GPIO.output(settings["red_pin"], GPIO.HIGH)
    GPIO.output(settings["green_pin"], GPIO.LOW)
    GPIO.output(settings["blue_pin"], GPIO.HIGH)


def lightBlue(settings):
    GPIO.output(settings["red_pin"], GPIO.LOW)
    GPIO.output(settings["green_pin"], GPIO.HIGH)
    GPIO.output(settings["blue_pin"], GPIO.HIGH)


change_color = {
    'off': turnOff,
    'white': white,
    'red': red,
    'green': green,
    'blue': blue,
    'yellow': yellow,
    'purple': purple,
    'lightBlue': lightBlue
}