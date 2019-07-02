import json
import random
from random import shuffle

import yaml

data_path = 'Data/TarotIndex.tsv'
tarot_path = 'Data/TarotCht.json'
tarot_en_path = 'Data/TarotEng.json'
trans_path = 'Data/TarotTranslate.txt'
trans_idx_path = 'Data/TarotIndex.tsv'

# Load tarot index info
tarot_idx = dict()
tarot_idxr = dict()
tarot_cht_eng = dict()
with open(data_path, 'r', encoding='UTF-8') as fin:
    for line in fin:
        i, _, n = line.strip().split('\t')
        tarot_idx[i] = n
        tarot_idxr[n] = i

# Load tarot json data.
tarot_data = json.load(open(tarot_path, 'r', encoding='UTF-8'))

# Load eng tarot json data.
tarot_en_data = json.load(open(tarot_en_path, 'r', encoding='UTF-8'))

# Load config
with open('./config.yaml', 'r', encoding='UTF-8') as fin:
    config = yaml.load(fin, Loader=yaml.BaseLoader)

# Get translate info string.
translate_info = ""
with open(trans_path, 'r', encoding='UTF-8') as fin:
    for line in fin:
        translate_info += line
translate_info = [translate_info, "大阿卡納牌使用翻譯請參考\nhttps://tinyurl.com/TarotTranslate"]

# Get cht card name map to eng card name
with open(trans_idx_path, 'r', encoding='UTF-8') as fin:
    for line in fin:
        s = line.strip().split('\t')
        tarot_cht_eng[s[2]] = s[1]

# Get a random tarot img
def get_rand_tarot():
    i = random.randint(0, 77)
    return "https://%s:%s/tarot/%.2d.jpg" % (config['domain'], config['port'], i)

# Get img url by id
def get_img_by_id(i):
    return "https://%s:%s/tarot/%.2d.jpg" % (config['domain'], config['port'], i)

# Get many random tarot id
def get_shuffle_deck(n):
    deck = [i for i in range(0, 78)]
    shuffle(deck)
    if n > 78: n = 78
    return deck[:n]

# id should be formed in '%.2d' string
def id2name(id):
    if type(id) == int:
        id = '%.2d' % id
    return tarot_idx[id]

def file2name(file):
    try: i = int(file[:2])
    except: return None
    return id2name('%.2d' % i)

def name2id(name):
    try: return tarot_idxr[name]
    except: return None

def getKeywordByID(id):
    try: return tarot_data[id]['positive']['related'] + tarot_data[id]['positive']['behavior']
    except: return None

def getMeaningByID(id):
    try: return tarot_data[id]['positive']['meaning']
    except: return None

def en_getKeywordByID(id):
    try: return tarot_en_data[id]['positive']['related']
    except: return None

def getEnNameByChtName(n):
    try: return tarot_cht_eng[n]
    except:
        print("What is", n)
        return None

def getTranslate():
    return translate_info

if __name__ == "__main__":
    print(id2name("00"))
    print(id2name(0))
    print(file2name("00.jpg"))
    print(file2name("not a tarot.jpg"))
    print(tarot_data['00']['positive']['related'])
    print(get_shuffle_deck(10))
    print(en_getKeywordByID("05"))
