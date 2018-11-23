import json, random

class FortuneModule:
	def __init__(self):
		self.load_json()
	
	def load_json(self):
		self.fortune = json.load(open('Data/Fortune.json', 'r', encoding='utf8'))
	
	def get_fortune(self):
		return self.fortune[random.randint(0, len(self.fortune) - 1)]

	def get_fortune_format(self, target):
		f = self.get_fortune()
		s = ["【%s】「 %s」" % (f['type'], f['poem']), "解釋：「%s」" % f['explain']]
		if f['result'].get(target): s.append("%s如何：%s" % (target, f['result'][target]))
		if f['note']: s.append(f['note'])
		return s

if __name__ == '__main__':
	fm = FortuneModule()
	f = fm.get_fortune_format('交往')
	print(f)