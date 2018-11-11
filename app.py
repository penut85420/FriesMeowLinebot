# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

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
    if msg.lower() == 'suitcase':
        img_msg = ImageSendMessage(
            original_content_url='https://i.imgur.com/US1paQe.jpg',
            preview_image_url='https://i.imgur.com/US1paQes.jpg'
        )
        line_bot_api.reply_message(event.reply_token, [txt_msg, img_msg])
    else:
        line_bot_api.reply_message(event.reply_token, txt_msg)

if __name__ == "__main__":
    app.run(host='10.0.2.15', port='5000', debug=True, ssl_context=(
        '/etc/letsencrypt/live/daoppailoli.ddns.net/fullchain.pem', 
        '/etc/letsencrypt/live/daoppailoli.ddns.net/privkey.pem'))
