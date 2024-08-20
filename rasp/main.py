import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests


# Define o tipo de sensor
pino_bomba = 26
endpoint = "http://192.168.234.185:8000/"
dht_device = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temp = dht_device.temperature
        umid = dht_device.humidity
        if umid is not None and temp is not None:
            # postar as informações no endpoint
            try:
                print(temp, umid)
                requests.post(endpoint, json={"temperature": temp, "humidity": umid})
            except:
                print("Erro ao postar dados")
            time.sleep(5)
        elif umid is None or temp is None:
            print("Erro ao ler sensor")
            time.sleep(5)
    except:
        print("Erro ao ler sensor")
    GPIO.cleanup()
