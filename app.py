# -*- coding: utf-8 -*-
import importlib
import random
import re
from datetime import datetime

import yaml
from flask import Flask, abort, request, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)

PhotoManager = importlib.import_module('PhotoManager')
FriesChatbot = importlib.import_module('FriesChatbot')
DatabaseManager = importlib.import_module('DatabaseManager')
TarotModule = importlib.import_module('TarotModule')
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
    r = bot.response(msg, uid)
    msg_list = list()
    log_list = list()
    while i < len(r):
        if r[i] == True:
            i += 1
            msg_list.append(ImageSendMessage(original_content_url=r[i], preview_image_url=r[i]))
            n = file_pattern.search(r[i]).group("name")
            m = TarotModule.file2name(n)
            if m: 
                log_list.append("[Tarot Img]" + m)
                print("[Send Tarot]", m)
            else: 
                log_list.append(n)
                print("[Send Photo]", n)
        else:
            msg_list.append(TextSendMessage(text=r[i]))
            log_list.append(r[i])
            print("[Send Msg]", r[i])
        i += 1
    line_bot_api.reply_message(event.reply_token, msg_list)
    dbm.insert_msg_log([dt, uid, msg, str(log_list)])

def log(event):
    user_id = event.source.user_id
    dt = datetime.now()
    name = "User"
    try: name = line_bot_api.get_profile(user_id).display_name
    except: print("[Error] User profile not found")
    print("[Receive]", dt.strftime("[%Y/%m/%d %H:%M:%S]"), name, user_id)
    print("[Message]", event.message.text)
    return dt, user_id, event.message.text.replace("＃", "#")

if __name__ == "__main__":
    app.run(host='10.0.2.15', port='5000', debug=True
        , ssl_context=(config['cert'], config['key']))
    # app.run()
