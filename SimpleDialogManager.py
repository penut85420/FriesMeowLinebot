import json
import random
import re


class PatternItem:
    def __init__(self, reg, res):
        self.reg = reg
        self.res = res
    
    def match(self, msg):
        for reg in self.reg:
            if re.match(reg, msg, re.I):
                return True
        return False
    
    def get_res(self):
        r = random.randint(0, len(self.res) - 1)
        return self.res[r]

class SimpleDialogManager:
    def __init__(self):
        self.load_json()
    
    def load_json(self):
        data = json.load(open('Data/SimpleDialog.json', 'r', encoding='utf8'))
        self.pattern = list()
        for p in data:
            self.pattern.append(PatternItem(p['reg'], p['res']))
    
    def get_res(self, msg):
        for p in self.pattern:
            if p.match(msg):
                return p.get_res()
        return None

if __name__ == "__main__":
    sdm = SimpleDialogManager()
    msg_list = [
        "召喚威廷",
        "hello",
    ]
    for msg in msg_list:
        print(sdm.get_res(msg))
