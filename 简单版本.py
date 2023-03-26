import requests
from lxml import etree
import time
import re
import json
import random


def get_tunnel_proxies():
    proxy_host = "tunnel5.qg.net:12061"
    proxy_username = "63FDDEDB"
    proxy_pwd = "36C0A0F4D4C8"

    return {
        "http": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
        "https": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
    }


url = "https://api.bilibili.com/x/click-interface/click/web/h5"
first_url = "https://www.bilibili.com/video/BV12s4y1S7PQ"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
ctime = int(time.time())
data = {
    "part": 1,
    "lv": 0,
    "ftime": ctime - random.randint(100, 500),
    "stime": ctime,
    "type": 3,
    "sub_type": 0,
    "refer_url": "",
    "spmid": "333.788.0.0,",
    "from_spmid": "",
    "csrf": ""
}
sum = 0
while True:
    try:
        proxies = get_tunnel_proxies()
        page_text = requests.get(first_url, headers, proxies=proxies).text
        r = r'embedPlayer":(.+)},"upData":{"mid"'
        str_map = re.findall(r, page_text)[0]
        jsonp = json.loads(str_map)
        cid = jsonp["cid"]
        aid = jsonp["aid"]
        data["aid"] = aid
        data["cid"] = cid
        html = etree.HTML(page_text)
        player_num = html.xpath('//*[@id="viewbox_report"]/div/div/span[1]/@title')[0]
        print(player_num, "即将发送播放请求")
        res = requests.post(url=url, data=data, headers=headers, proxies=proxies)
        sum = sum + 1
        print(f"已经发送了{sum}次播放请求")
        time.sleep(1)
    except Exception as e:
        pass
