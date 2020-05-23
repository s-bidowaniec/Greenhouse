#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath("/home/pi/Scripts/HK-47-IoT/"))
import datetime
import time
from slack import RTMClient
from secrets import slack_token
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
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
        if 'hello' in data['text'].lower():
            response(f"Hi!")
        elif 'podlej' in data['text'].lower():
            try:
                num = int(data['text'].split()[0])
            except:
                num = 60
            response("podlewanie rozpoczęte {}, na {} minut.".format(datetime.datetime.now(), num))
            GPIO.output(15,GPIO.HIGH)
            time.sleep(num*60)
            GPIO.output(15,GPIO.LOW)
            response("podlewanie zakonczone {}".format(datetime.datetime.now()))
        elif 'wentyluj' in data['text'].lower():
            try:
                num = int(data['text'].split()[0])
            except:
                num = 60
            response("wentylowanie rozpoczęte {}, na {} minut".format(datetime.datetime.now(), num))
            GPIO.output(18,GPIO.HIGH)
            time.sleep(num*60)
            GPIO.output(18,GPIO.LOW)
            response("wentylowanie zakonczone {}".format(datetime.datetime.now()))
        elif 'stop' in data['text'].lower():
            GPIO.output(18,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)
        elif 'raport' in data['text'].lower():
            humidity_air, temperature_air = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            humidity_ground = mcp.read_adc(0)
            if humidity_ground is None:
                response("Czujnik wilgotnosci gleby nie odpowiada")
            elif humidity is not None and temperature is not None:
                response("Wilgotność gruntu wynosi {}%, temperatura powietrza wynosi {0:0.1f}C natomiast wilgotność powietrza {1:0.1f}%".format(humidity_ground, temperature_air, humidity_air))
            else:
                response("Czujnik DHT nie odpowiada")

rtm_client = RTMClient(token=slack_token)
rtm_client.start()
