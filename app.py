# -*- coding: utf-8 -*-
import random
import yaml
import importlib
from flask import Flask, abort, request, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)

PhotoManager = importlib.import_module('PhotoManager')

app = Flask(__name__)

config = yaml.load(open('config.yaml', 'r', encoding='utf8'))
line_bot_api = LineBotApi(config['token'])
h = WebhookHandler(config['channel'])

@app.route("/")
def hello():
    return "Meow Meow Meow"

@app.route('/images/<string:pid>')
def get_image(pid):
    return send_file('Images/%s' % pid, mimetype='image/png')


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    try:
        h.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@h.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '喵' * random.randint(2, len(msg))
    img_path = PhotoManager.rand_img()
    img_url = 'https://daoppailoli.ddns.net:5000/images/' + img_path
    txt_msg = TextSendMessage(r)
    img_msg = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.reply_message(event.reply_token, [txt_msg, img_msg])

if __name__ == "__main__":
    # app.run(host='10.0.2.15', port='5000', debug=True, ssl_context=(
    #     '/etc/letsencrypt/live/daoppailoli.ddns.net/fullchain.pem', 
    #     '/etc/letsencrypt/live/daoppailoli.ddns.net/privkey.pem'))
    app.run()
