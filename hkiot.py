import os
import datetime
from slack import RTMClient




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

slack_token = os.environ['SLACK_BOT_TOKEN']
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
