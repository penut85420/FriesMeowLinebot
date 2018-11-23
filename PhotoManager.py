import os, random

def rand_img():
    for _, _, flist in os.walk('Images/'):
        return flist[random.randint(0, len(flist) - 1)]