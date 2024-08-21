import RPi.GPIO as gpio
import time

pin = 3
gpio.setmode(gpio.BCM)

gpio.setup(pin, gpio.IN)

if gpio.input(pin) == gpio.LOW:
	print('nao')
else:
	print('sim')

gpio.cleanup()

