import re
url1 = r"https://daoppailoli.ddns.net:5000/images/P_20180408_142950_vHDR_On.jpg"
url2 = r"https://daoppailoli.ddns.net:5000/tarot/00.png"
reg = "https.*//?(?P<name>.*\\.(.*))"
m = re.search(reg, url1).group("name")
print(m)