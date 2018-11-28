# -*- coding: utf-8 -*- 
import importlib
import random

import PhotoManager
import TarotModule
from DatabaseManager import DatabaseManager
from FortuneModule import FortuneModule
from SimpleDialogManager import SimpleDialogManager

# FortuneModule = importlib.import_module('FortuneModule')
# PhotoManger = importlib.import_module('PhotoManager')
# TarotModule = importlib.import_module('TarotModule')
# DatabaseManager = importlib.import_module('DatabaseManager')
# SimpleDialogManager = importlib.import_module('SimpleDialogManager')

class FriesChatbot:
	def __init__(self):
		self.fortune = FortuneModule()
		self.dbm = DatabaseManager()
		self.sdm = SimpleDialogManager()
		self.function_map = {
			'#召喚貓貓': self.function_photo,
			'#貓貓籤筒': self.function_fortune,
			'#貓貓塔羅': self.function_tarot,
			'#貓貓解牌': self.function_explain,
		}
	
	def response(self, msg, uid):
		if not msg.startswith('#'): return None
		cmd = msg.split()[0]
		if self.function_map.get(cmd):
			return self.function_map[cmd](msg, uid)
		return self.function_simple_dialog(msg, uid)
		# return ['#召喚貓貓 #貓貓籤筒 #貓貓塔羅 #貓貓解牌']

	def function_photo(self, msg, uid):
		return [
			"熱騰騰的薯條照片來囉~" + '喵' * random.randint(1, len(msg)),
			True, PhotoManager.rand_imgurl()
		]
	
	def function_fortune(self, msg, uid):
		seg = msg.split()
		if len(seg) < 2:
			seg.append("~")
		target = seg[1]
		if target == '?':
			return ["可以跟貓貓籤筒詢問願望、疾病、遺失物、盼望的人、蓋新居、搬家、旅行、結婚、交往的事喔ωωω"]
		return self.fortune.get_fortune_format(target)

	def function_tarot(self, msg, uid):
		arg = msg.split()
		if len(arg) < 2:
			arg.append(1)
		n = 0
		try: n = int(arg[1])
		except: n = 1
		if n > 78: n = 78
		if n < 1: n = 1
		rtn = list()
		if n <= 5:
			for i in TarotModule.get_shuffle_deck(n):
				rtn.append(True)
				rtn.append(TarotModule.get_img_by_id(i))
		else:
			deck = TarotModule.get_shuffle_deck(n)
			msg = TarotModule.id2name(deck[0])
			for i in deck[1:]:
				msg += "、" + TarotModule.id2name(i)
			rtn.append(msg)
		return rtn

	def function_explain(self, msg, uid):
		arg = msg.split()
		rtn_list = list()
		m = len(arg)
		if m > 1 and arg[1] == '翻譯':
			for item in TarotModule.getTranslate():
				rtn_list.append(item)
		elif m > 1:
			if m > 6: m = 6
			for i in arg[1:m]:
				card = TarotModule.getKeywordByID(TarotModule.name2id(i))
				if card: rtn_list.append("「%s」代表：%s" % (i, card))
				else:
					rtn_list.append("找不到「%s」的說\n如果是小阿卡納牌（寶劍、權杖、聖杯、錢幣）要把數量詞或宮廷人物放在後面喔~\n例如：寶劍三、聖杯王后" % i)
		else:
			last_tarot = self.dbm.get_lastest_tarot([uid])
			if len(last_tarot) == 0:
				rtn_list.append("請告訴我你想解的牌，例如：#貓貓解牌 寶劍騎士")
			else:
				query = "#貓貓解牌"
				for i in last_tarot:
					query += " " + i
				return self.function_explain(query, uid)
		#return TarotModule.getKeywordByID(TarotModule.name2id(arg[1]))
		return rtn_list

	def function_simple_dialog(self, msg, uid):
		return [self.sdm.get_res(msg[1:])]

if __name__ == "__main__":
	fc = FriesChatbot()
	uid = 'U3c70a0e93aaa36c5643ab480f7f1a023'
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
		"#貓貓解牌 聖杯國王",
		"#貓貓解牌 聖杯國王 世界",
		"#貓貓解牌 聖杯國王 權杖王后 寶劍侍者 錢幣騎士 惡魔 戀人",
		"#貓貓解牌",
		"#貓貓解牌 翻譯",
		"#貓貓解牌 沒這張牌",
		"#貓貓解牌 看不懂",
		"#召喚威廷",
		"#貓貓塔羅 10",
		"#貓貓塔羅 20",
		"#嗨",
		"#召喚孫全",
	]
	for s in msg_list:
		print(fc.response(s, uid))
