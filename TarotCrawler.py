import requests
url = 'http://www.looktarot.com/images/tarot/225_%.2d.jpg'
for i in range(0, 78):
    with open('Tarot/%.2d.jpg' % i, 'wb') as fout:
        fout.write(requests.get(url % i).content)