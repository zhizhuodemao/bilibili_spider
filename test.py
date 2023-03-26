import json
import requests
import re
session = requests.session()

v2_url = f"https://api.bilibili.com/x/player/wbi/v2"
v2_resp = session.get(url=v2_url)
print(v2_resp.json())

re=session.get("https://baidu.com")
print(re.text)