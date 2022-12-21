import RPi.GPIO as GPIO
from time import sleep
from enum import Enum

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class Pin(Enum):
    UP = 8
    DOWN = 10
    LEFT = 13
    RIGHT = 15


class PinHandler:

    def __init__(self):
        GPIO.setup(Pin.UP.value, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.DOWN.value, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.LEFT.value, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.RIGHT.value, GPIO.OUT, initial=GPIO.LOW)

    @staticmethod
    def up_on():
        GPIO.output(Pin.UP.value, GPIO.HIGH)

    @staticmethod
    def up_off():
        GPIO.output(Pin.UP.value, GPIO.LOW)

    @staticmethod
    def down_on():
        GPIO.output(Pin.DOWN.value, GPIO.HIGH)

    @staticmethod
    def down_off():
        GPIO.output(Pin.DOWN.value, GPIO.LOW)

    @staticmethod
    def left_on():
        GPIO.output(Pin.LEFT.value, GPIO.HIGH)

    @staticmethod
    def left_off():
        GPIO.output(Pin.LEFT.value, GPIO.LOW)

    @staticmethod
    def right_on():
        GPIO.output(Pin.RIGHT.value, GPIO.HIGH)

    @staticmethod
    def right_off():
        GPIO.output(Pin.RIGHT.value, GPIO.LOW)


pin_handler = PinHandler()

