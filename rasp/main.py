import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests


# Define o tipo de sensor
pino_bomba = 26
endpoint = 'http://localhost:8000/temperature'
dht_device = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temp = dht_device.temperature
        umid = dht_device.humidity
        if umid is not None and temp is not None:
            print (temp, umid)
            time.sleep(5)
        elif umid is None or temp is None:
            print('Erro ao ler sensor')
            time.sleep(5)
    except:
        print('Erro ao ler sensor')
    GPIO.cleanup()

