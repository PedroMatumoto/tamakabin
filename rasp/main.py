import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient


# Define o tipo de sensor
pino_bomba = 26
endpoint = "https://df54-2804-18-903-123-c459-b01c-1714-9b23.ngrok-free.app/api/data"
#client = MongoClient(uri)
#database = client["tomferrite"]
#collection = database["enzosakamoto"]
dht_device = adafruit_dht.DHT22(board.D4)
PIN=3
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN,GPIO.IN)


try:
    while True:
        try:
            temp = dht_device.temperature
            umid = dht_device.humidity
            print('ta aqui')
            bright = GPIO.input(PIN)

            if umid is not None and temp is not None:
                # postar as informações no endpoint
                #try:
                #    result = collection.insert_one({"temperature": temp, "umidity": umid})
                #    print(result.acknowledged)
                #except Exception as e:
                #    print(e)
                try:
                    print(temp, umid)
                    #
                    requests.post(endpoint, json={"temperature": temp, "umidity": umid, "brightness":bright})
                except Exception as e:
                    print(e)
                    print("Erro ao postar dados")
                time.sleep(5)
            elif umid is None or temp is None:
                print("Erro ao ler sensor")
                time.sleep(5)
        except:
            print("Erro ao ler sensor")
except:
    GPIO.cleanup()

