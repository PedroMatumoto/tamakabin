import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import board
import time
import requests
# from pymongo.mongo_client import MongoClient
# from pydantic import BaseModel
# from motor.motor_asyncio import AsyncIOMotorClient
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image
from PIL import ImageDraw

# Define o tipo de sensor
pino_bomba = 20
endpoint = "http://tamakabin.vercel.app/api/data"
# client = MongoClient(uri)
# database = client["tomferrite"]
# collection = database["enzosakamoto"]
beatmap = [
    ['❄️', '🥶', '🌞', '🔥'],
    ['🌵', '☀️', '🌅', '🌞'],
    ['🌙', '🌌', '🌜', '🌟']
]

PIN = 4
GPIO.setmode(GPIO.BCM)
sensor = dht.DHT22
GPIO.setup(PIN, GPIO.IN)
GPIO.setup(pino_bomba, GPIO.OUT)
DHT = 21


serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Preparacoes necessarias para apagar tela
icone_frio = (
    Image.open("assets/icone_frio.png").convert("1")
)
icone_frio = icone_frio.resize(device.size)
icone_quente = (
    Image.open("assets/icone_quente.png").convert("1")
)
icone_quente = icone_quente.resize(device.size)
icone_seco = (
    Image.open("assets/icone_seco.png").convert("1")
)
icone_seco = icone_seco.resize(device.size)
icone_sol = (
    Image.open("assets/icone_sol.png").convert("1")
)
icone_sol = icone_sol.resize(device.size)
icone_nuvem = (
    Image.open("assets/icone_nuvem.png").convert("1")
)
icone_nuvem = icone_nuvem.resize(device.size)

try:
    while True:
        try:
            umid, temp = dht.read_retry(sensor,DHT)
            bright = GPIO.input(PIN)
            if umid is not None and temp is not None:
                print('info not null')
		# postar as informações no endpoint
                # try:
                #    result = collection.insert_one({"temperature": temp, "umidity": umid})
                #    print(result.acknowledged)
                # except Exception as e:
                #    print(e)
                try:
                    print(temp, umid, bright)
                    temp = round(temp,2)
                    umid = round(umid,2)
                    response = requests.post(
                        endpoint,
                        json={
                            "temperature": temp,
                            "umidity": umid,
                            "brightness": bright,
                        },
                    )
                    print(response)
                    
                except Exception as e:
                    print(e)
                    print("Erro ao postar dados")
                time.sleep(5)

                if umid < 40:
                    print("Muito seco")
                    GPIO.output(pino_bomba, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(pino_bomba, GPIO.LOW)
                    with canvas(device) as draw:
                        draw.text((0, 0), f"Muito Seco!\nRegando...", fill=255)

                elif temp < 20:
                    print("frio")
                    device.display(icone_frio)
                    with canvas(device) as draw:
                        draw.text((0, 0), f"Muito frio!\nMe coloque pra dentro!", fill=255)

                elif temp > 30:
                    print("calor")
                    with canvas(device) as draw:
                        draw.text((0, 0), f"Muito Calor!\nMe coloque tire do sol!", fill=255)

                elif (
                    bright == 0
                    and time.localtime().tm_hour > 6
                    and time.localtime().tm_hour < 18
                ):
                    print("luz de dia")
                    with canvas(device) as draw:
                        draw.text((0, 0), f"Sol! Ainda bem!", fill=255)

                elif (
                    bright == 1
                    or time.localtime().tm_hour < 6
                    or time.localtime().tm_hour > 18
                ):
                    print("eita ta de noite")
                    with canvas(device) as draw:
                       draw.text((0, 0), f"Noite! Vou dormir...", fill=255)

                else:
                    print("tudo ok")
                    disp.clear()
                    with canvas(device) as draw:
                        draw.text((0, 0), f"Tudo ok", fill=255)
                        draw.text((0, 0), f"Temperatura: {temp}°C", fill=255)
                        draw.text((0, 10), f"Umidade: {umid}%", fill=255)
                        draw.text((0, 20), f"Luminosidade: {bright}", fill=255)

            elif umid is None or temp is None:
                print("Erro ao ler sensor")
                time.sleep(5)
        except Exception as e:
            print("Erro na parte sensor")
            print(e)
except:
    GPIO.cleanup()
