import os, random

def rand_img():
    for _, _, flist in os.walk('Images/'):
        return flist[random.randint(0, len(flist) - 1)]
    return 'P_20180408_142950_vHDR_On.jpg'

def rand_imgurl():
    return 'https://daoppailoli.ddns.net:5000/images/' + rand_img()