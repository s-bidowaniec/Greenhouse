#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath("/home/pi/Scripts/HK-47-IoT/"))
import datetime
from slack import RTMClient
from secrets import slack_token
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']

    def response(text):
        text = str(text)
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=thread_ts
        )
    if 'text' in data.keys():
        if 'Hello' in data['text']:
            response(f"Hi!")
        elif 'time' in data['text']:
            response(datetime.datetime.now())
        elif 'pokrzywa' in data['text']:
            value = mcp.read_adc(0)
            response("w doniczce wilgotność wynosi około {}%".format(value/4))
        elif 'on' in data['text']:
            GPIO.output(18,GPIO.HIGH)
        elif 'off' in data['text']:
            GPIO.output(18,GPIO.LOW)
        elif 'pogoda' in data['text']:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                response("Temperatura powietrza wynosi {0:0.1f}C natomiast wilgotność {1:0.1f}%".format(temperature, humidity))
            else:
                response("Czujnik DHT nie odpowiada")

rtm_client = RTMClient(token=slack_token)
rtm_client.start()
