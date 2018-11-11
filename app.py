# -*- coding: utf-8 -*-
import random

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)

app = Flask(__name__)
img_list = []
with open('imglist.txt', 'r', encoding='utf-8') as fin:
    for line in fin:
        img_list.append(line.strip())
line_bot_api = LineBotApi('QIFODrc39Bd4bilZeOR3H/fZmeSKgRHxDl5EmY3U1dv4XES9pkEVATBqrmplpxIDqe/HE1lQ/4ieUpG5GuF0icB1DqT64UFyb+0qQvgVdzuu0wSkVR9V89p63x2sGPEQQJ9C9SiKyNBpA+i8SfJVqQdB04t89/1O/w1cDnyilFU=')
h = WebhookHandler("a41365f312eeaad6a885e44efd59f25b")

@app.route("/")
def hello():
    return "Meow Meow Meow"

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        h.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@h.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '喵' * len(msg)
    txt_msg = TextSendMessage(r)
    org, pre = get_random_photo()
    
    img_msg = ImageSendMessage(original_content_url=org, preview_image_url=pre)
    line_bot_api.reply_message(event.reply_token, [txt_msg, img_msg])

def get_random_photo():
    r = random.randint(0, len(img_list))
    s1 = img_list[r] + ".jpg"
    s2 = img_list[r] + "s.jpg"
    return s1, s2

if __name__ == "__main__":
    app.run(host='10.0.2.15', port='5000', debug=True, ssl_context=(
        '/etc/letsencrypt/live/daoppailoli.ddns.net/fullchain.pem', 
        '/etc/letsencrypt/live/daoppailoli.ddns.net/privkey.pem'))
