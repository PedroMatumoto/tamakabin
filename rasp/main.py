import fastapi
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import requests


# Define o tipo de sensor
pino_sensor = 25
pino_bomba = 26
endpoint = 'http://localhost:8000/temperature'


while True:
    sensor = Adafruit_DHT.DHT11
    GPIO.setmode(GPIO.BOARD)
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
    if umid is not None and temp is not None:
        print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}n").format(temp, umid);
        requests.post(endpoint, json={'temperature': temp, 'humidity': umid})
        time.sleep(5);
    elif umid is None or temp is None:
        print('Erro ao ler sensor')
        requests.post(endpoint, json={'temperature': 'error', 'humidity': 'error'})
        time.sleep(5)
    
    # caso a umidade esteja abaixo de 30% liga a bomba
    if umid < 30:
        GPIO.setup(pino_bomba, GPIO.OUT)
        GPIO.output(pino_bomba, GPIO.HIGH)
    elif umid > 30:
        GPIO.output(pino_bomba, GPIO.LOW)

    GPIO.cleanup()


