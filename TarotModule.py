import random, json

data_path = 'Data/TarotIndex.tsv'
tarot_path = 'Data/TarotCht.json'
trans_path = 'Data/TarotTranslate.txt'
tarot_idx = dict()
tarot_idxr = dict()
with open(data_path, 'r', encoding='utf8') as fin:
    for line in fin:
        i, _, n = line.strip().split('\t')
        tarot_idx[i] = n
        tarot_idxr[n] = i

tarot_data = json.load(open(tarot_path, 'r', encoding='utf8'))

translate_info = ""
with open(trans_path, 'r', encoding='utf8') as fin:
    for line in fin:
        translate_info += line

def get_rand_tarot():
    i = random.randint(0, 77)
    return "https://daoppailoli.ddns.net:5000/tarot/%.2d.jpg" % i

def id2name(id):
    if type(id) == int:
        id = '%.2d' % id
    return tarot_idx[id]

def file2name(file):
    try: 
        i = int(file[:2])
    except: return None
    return id2name('%.2d' % i)

def name2id(name):
    try: return tarot_idxr[name]
    except: return None

def getKeywordByID(id):
    try: return tarot_data[id]['positive']['related']
    except: return None

def getTranslate():
    return translate_info

if __name__ == "__main__":
    print(id2name("00"))
    print(id2name(0))
    print(file2name("00.jpg"))
    print(file2name("not a tarot.jpg"))
    print(tarot_data['00']['positive']['related'])

    