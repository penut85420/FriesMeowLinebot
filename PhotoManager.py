import os
import random

import yaml

with open('./config.yaml', 'r', encoding='UTF-8') as fin:
    config = yaml.load(fin, Loader=yaml.BaseLoader)

def rand_img():
    for _, _, flist in os.walk('Images/'):
        return flist[random.randint(0, len(flist) - 1)]
    return 'P_20180408_142950_vHDR_On.jpg'

def rand_imgurl():
    return 'https://%s:%s/images/%s' % (config['domain'], config['port'], rand_img())
