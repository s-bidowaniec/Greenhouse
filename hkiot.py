import os
import datetime
from slack import RTMClient
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


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
        if 'time' in data['text']:
            response(datetime.datetime.now())
        if 'pokrzywa' in data['text']:
            value = mcp.read_adc(0)
            response("w doniczce wilgotność wynosi około {}%".format(value/4))

slack_token = os.environ['SLACK_BOT_TOKEN']
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
