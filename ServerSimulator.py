import random
import importlib
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)
FriesChatbot = importlib.import_module('FriesChatbot')
bot = FriesChatbot.FriesChatbot()
def sim(msg):
    # log(event)
    i = 0
    r = bot.response(msg)
    print(r, len(r))
    msg_list = list()
    while i < len(r):
        print(i, r[i])
        if r[i] == True:
            i += 1
            print(i, end='')
            try:
                print('Here is a photo', r[i])
                msg_list.append(ImageSendMessage(original_content_url=r[i], preview_image_url=r[i]))
            except Exception as e:
                print("Error in app.py:", e)
        else:
            msg_list.append(TextSendMessage(text=r[i]))
        i += 1
    # line_bot_api.reply_message(event.reply_token, msg_list)

if __name__ == "__main__":
    sim("#貓貓籤筒")