# -*- coding: utf-8 -*- 
import importlib, random

FortuneModule = importlib.import_module('FortuneModule')
PhotoManger = importlib.import_module('PhotoManager')
TarotModule = importlib.import_module('TarotModule')

class FriesChatbot:
	def __init__(self):
		self.fortune = FortuneModule.FortuneModule()
		self.function_map = {
			'#貓貓籤筒': self.function_fortune,
			'#召喚貓貓': self.function_photo,
			'#貓貓塔羅': self.function_tarot,
		}
	
	def response(self, msg):
		if not msg.startswith('#'): return None
		cmd = msg.split()[0]
		if self.function_map.get(cmd):
			return self.function_map[cmd](msg)
		return ['#召喚貓貓 #貓貓籤筒 #貓貓塔羅']

	def function_photo(self, msg):
		return [
			"熱騰騰的薯條照片來囉~" + '喵' * random.randint(1, len(msg)),
			True, PhotoManger.rand_imgurl()
		]
	
	def function_fortune(self, msg):
		seg = msg.split()
		if len(seg) < 2:
			seg.append("~")
		target = seg[1]
		if target == '?':
			return ["可以跟貓貓籤筒詢問願望、疾病、遺失物、盼望的人、蓋新居、搬家、旅行、結婚、交往的事喔ωωω"]
		return self.fortune.get_fortune_format(target)

	def function_tarot(self, msg):
		arg = msg.split()
		if len(arg) < 2:
			arg.append(1)
		n = 0
		try:
			n = int(arg[1])
		except:
			n = 1
		if n > 5:
			n = 5
		rtn = list()
		for _ in range(0, n):
			rtn.append(True)
			rtn.append(TarotModule.get_rand_tarot())
		return rtn

if __name__ == "__main__":
	fc = FriesChatbot()
	msg_list = [
		'#召喚貓貓',
		"#貓貓籤筒 交往",
		"#貓貓籤筒",
		"#貓貓籤筒 ?",
		"#貓貓塔羅",
		"#貓貓塔羅 3",
		"#貓貓塔羅 5",
		"#貓貓塔羅 7",
		"#貓貓塔羅 來亂",
		"#沒這功能",
	]
	for s in msg_list:
		print(fc.response(s))
