# -*- coding: utf-8 -*- 
import importlib, random

FortuneModule = importlib.import_module('FortuneModule')
PhotoManger = importlib.import_module('PhotoManager')

class FriesChatbot:
	def __init__(self):
		self.fortune = FortuneModule.FortuneModule()
		self.function_map = {
			'#貓貓籤筒': self.function_fortune,
			'#召喚貓貓': self.function_photo,
		}
	
	def response(self, msg):
		if not msg.startswith('#'): return None
		cmd = msg.split()[0]
		return self.function_map[cmd](msg)

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

if __name__ == "__main__":
	fc = FriesChatbot()
	msg_list = [
		'#召喚貓貓',
		"#貓貓籤筒 交往",
		"#貓貓籤筒",
		"#貓貓籤筒 ?"
	]
	for s in msg_list:
		print(fc.response(s))