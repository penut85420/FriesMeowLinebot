import random

def get_rand_tarot():
    i = random.randint(0, 77)
    return "https://daoppailoli.ddns.net:5000/tarot/%.2d.jpg" % i