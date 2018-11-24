# -*- coding: utf-8 -*-
import random
import yaml
import importlib
import re
from datetime import datetime
from flask import Flask, abort, request, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)

PhotoManager = importlib.import_module('PhotoManager')
FriesChatbot = importlib.import_module('FriesChatbot')
DatabaseManager = importlib.import_module('DatabaseManager')
app = Flask(__name__)

config = yaml.load(open('config.yaml', 'r', encoding='utf8'))
line_bot_api = LineBotApi(config['token'])
h = WebhookHandler(config['channel'])
bot = FriesChatbot.FriesChatbot()
dbm = DatabaseManager.DatabaseManager()
file_pattern = re.compile("https.*//?(?P<name>.*\\.(.*))")

@app.route("/")
def hello():
    return "Meow Meow Meow"

@app.route('/images/<string:pid>')
def get_image(pid):
    return send_file('Images/%s' % pid, mimetype='image/png')

@app.route('/tarot/<string:pid>')
def get_tarot(pid):
    return send_file('Tarot/%s' % pid, mimetype='image/png')

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        h.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@h.add(MessageEvent, message=TextMessage)
def handle_message(event):
    dt, uid, msg = log(event)
    if not msg.startswith("#"): return
    i = 0
    r = bot.response(msg)
    msg_list = list()
    log_list = list()
    while i < len(r):
        print(i, r[i])
        if r[i] == True:
            i += 1
            msg_list.append(ImageSendMessage(original_content_url=r[i], preview_image_url=r[i]))
            log_list.append(file_pattern.search(r[i]).group("name"))
        else:
            msg_list.append(TextSendMessage(text=r[i]))
            log_list.append(r[i])
        i += 1
    line_bot_api.reply_message(event.reply_token, msg_list)
    dbm.insert_msg_log([dt, uid, msg, str(log_list)])

def log(event):
    profile = None
    user_id = None
    dt = datetime.now()
    try: 
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(user_id)
        print(dt, profile.display_name, user_id)
        print("[Receive]", event.message.text)
    except: pass
    return dt, user_id, event.message.text


if __name__ == "__main__":
    app.run(host='10.0.2.15', port='5000', debug=True, ssl_context=(
       '/etc/letsencrypt/live/daoppailoli.ddns.net/fullchain.pem', 
       '/etc/letsencrypt/live/daoppailoli.ddns.net/privkey.pem'))
    # app.run()
