import random

data_path = 'Data/TarotIndex.tsv'
fin = open(data_path, 'r', encoding='utf8')
tarot_idx = dict()
for line in fin:
    i, _, n = line.strip().split('\t')
    tarot_idx[i] = n

def get_rand_tarot():
    i = random.randint(0, 77)
    return "https://daoppailoli.ddns.net:5000/tarot/%.2d.jpg" % i

def id2name(id):
    if type(id) == int:
        id = '%.2d' % id