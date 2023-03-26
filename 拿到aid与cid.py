# "embedPlayer":
import json

import requests
import re

url = "https://www.bilibili.com/video/BV18c411L7wB/"
r = r'embedPlayer":(.+)},"upData":{"mid"'
resp = requests.get(url)
str_map = re.findall(r, resp.text)[0]
json = json.loads(str_map)
cid = json["cid"]
aid = json["aid"]
print(cid)
print(aid)
