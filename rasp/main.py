import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import requests
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw

# Define o tipo de sensor
pino_bomba = 26
endpoint = "https://tamakabin.vercel.app/api/data"
# client = MongoClient(uri)
# database = client["tomferrite"]
# collection = database["enzosakamoto"]

dht_device = adafruit_dht.DHT22(board.D4)
PIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

# Configura o display OLED
RST = (
    24  # embora nao utilizado de fato, eh preciso defini-lo para a biblioteca funcionar
)

# Configura uso do display OLED de 128x64 (comunicacao I²C)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Inicializa biblioteca de comunicacao com display e o limpa
disp.begin()
disp.clear()
disp.display()

# obtem altura e largura totais do display
width = disp.width
height = disp.height

# Preparacoes necessarias para apagar tela
icone_frio = (
    Image.open("assets/icone_frio")
    .resize((disp.width, disp.height), Image.ANTIALIAS)
    .convert("1")
)
icone_quente = (
    Image.open("assets/icone_quente")
    .resize((disp.width, disp.height), Image.ANTIALIAS)
    .convert("1")
)
icone_seco = (
    Image.open("assets/icone_seco")
    .resize((disp.width, disp.height), Image.ANTIALIAS)
    .convert("1")
)
icone_sol = (
    Image.open("assets/icone_sol")
    .resize((disp.width, disp.height), Image.ANTIALIAS)
    .convert("1")
)
icone_nuvem = (
    Image.open("assets/icone_nuvem")
    .resize((disp.width, disp.height), Image.ANTIALIAS)
    .convert("1")
)

image = Image.new("1", (width, height))  # imagem binaria (somente 1's e 0's)
draw = ImageDraw.Draw(image)


try:
    while True:
        try:
            temp = dht_device.temperature
            umid = dht_device.humidity
            print("ta aqui")
            bright = GPIO.input(PIN)

            if umid is not None and temp is not None:
                # postar as informações no endpoint
                # try:
                #    result = collection.insert_one({"temperature": temp, "umidity": umid})
                #    print(result.acknowledged)
                # except Exception as e:
                #    print(e)
                try:
                    print(temp, umid)
                    #
                    requests.post(
                        endpoint,
                        json={
                            "temperature": temp,
                            "umidity": umid,
                            "brightness": bright,
                        },
                    )
                except Exception as e:
                    print(e)
                    print("Erro ao postar dados")
                time.sleep(5)

                if umid < 40:
                    GPIO.output(pino_bomba, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(pino_bomba, GPIO.LOW)
                    disp.clear()
                    disp.display()
                    disp.image(icone_seco)

                elif temp < 20:
                    disp.clear()
                    disp.display()
                    disp.image(icone_frio)

                elif temp > 30:
                    disp.clear()
                    disp.display()
                    disp.image(icone_quente)

                elif (
                    bright == 1
                    and time.localtime().tm_hour > 6
                    and time.localtime().tm_hour < 18
                ):
                    disp.clear()
                    disp.display()
                    disp.image(icone_sol)

                elif (
                    bright == 0
                    or time.localtime().tm_hour < 6
                    or time.localtime().tm_hour > 18
                ):
                    disp.clear()
                    disp.display()
                    disp.image(icone_nuvem)

                else:
                    disp.clear()
                    disp.display()
                    draw.text((0, 0), f"Tudo ok", fill=255)
                    draw.text((0, 0), f"Temperatura: {temp}°C", fill=255)
                    draw.text((0, 10), f"Umidade: {umid}%", fill=255)
                    draw.text((0, 20), f"Luminosidade: {bright}", fill=255)

            elif umid is None or temp is None:
                print("Erro ao ler sensor")
                time.sleep(5)
        except:
            print("Erro ao ler sensor")
except:
    GPIO.cleanup()
