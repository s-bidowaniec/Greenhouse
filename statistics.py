#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath("/home/pi/Scripts/HK-47-IoT/"))
import datetime
import time
import pause
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

while True:
    time_full = (60 - datetime.datetime.now().minute)*60 - datetime.datetime.now().second
    time.sleep(time_full)
    humidity_ground = mcp.read_adc(0)/4
    if humidity_ground is None:
        humidity_ground = -999
    humidity_air, temperature_air = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity_air is None:
        humidity_air = -999
    if temperature_air is None:
        temperature_air = -999
    f = open("demofile2.txt", "a")
    f.write("{}, {}, {}, {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:00"), humidity_ground, humidity_air, temperature_air))
    f.close()
    time.sleep(5)
