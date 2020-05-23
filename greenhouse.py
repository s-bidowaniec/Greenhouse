#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath("/home/pi/Scripts/HK-47-IoT/"))
import datetime
import time
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
    humidity_air, temperature_air = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    humidity_ground = mcp.read_adc(0)/4
    if humidity_ground < 80:
        GPIO.output(15,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(15,GPIO.LOW)
    if temperature_air > 20 or humidity_air > 70:
        GPIO.output(18,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(18,GPIO.LOW)
    time.sleep(5)
