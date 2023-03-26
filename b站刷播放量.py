# 首先 我们要做的内容是刷播放量 我们应当先了解以下内容
# 1.只有点击播放按钮才算播放量 只加载视频不点播放不算播放量
# 2.点击播放之后应该是发送了一个请求 该请求后台收到之后可以会把数据库中播放量加1 我们要做的就是解析这个请求 发这个请求
# 3.每个视频应该是点击的那一瞬间发送的请求 并且只发送一次请求 因为播放量只增加一次
# 所以 我们应该在页面完全加载之后,视频还没开始播放的时候,点击播放按钮,看看发送了什么请求
import random

from lxml import etree
import json
import requests
import re
# 如果代码中有中文 把以下这段代码加入
import subprocess
from functools import partial
import time
import json

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import execjs


def get_tunnel_proxies():
    proxy_host = "tunnel5.qg.net:12061"
    proxy_username = "63FDDEDB"
    proxy_pwd = "36C0A0F4D4C8"

    return {
        "http": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
        "https": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
    }


def add_play_num(video_url, proxys):
    # 发送首页请求 拿到aid cid和cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    session = requests.session()

    resp = session.get(video_url, headers=headers, proxies=proxys)
    page_text = resp.text
    r = r'embedPlayer":(.+)},"upData":{"mid"'
    str_map = re.findall(r, page_text)[0]
    jsonp = json.loads(str_map)
    cid = jsonp["cid"]
    aid = jsonp["aid"]
    ctime = int(time.time())
    data = {
        "aid": aid,
        "cid": cid,
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
    with open("get_cookies.js", "r", encoding="utf-8") as f:
        fn = f.read()

    js = execjs.compile(fn)
    uuid = js.call("get_uuid")
    b_lsid = js.call("get_b_lsid")
    session.cookies.set("CURRENT_FNVAL", "4048")
    v2_url = f"https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}"
    session.get(v2_url, proxies=proxys)
    session.cookies.set("_uuid", uuid)
    session.cookies.set("b_lsid", b_lsid)
    spi_url = "https://api.bilibili.com/x/frontend/finger/spi"
    spi_resp = session.get(spi_url, proxies=proxys)
    buvid4 = spi_resp.json()["data"]["b_4"]
    session.cookies.set("buvid4", buvid4)
    session.cookies.set("buvid_fp", "cff8043e43d0cb70fb53b2f86c2511e1")
    h5_url = "https://api.bilibili.com/x/click-interface/click/web/h5"
    html = etree.HTML(page_text)
    player_num = html.xpath('//*[@id="viewbox_report"]/div/div/span[1]/@title')[0]
    print("当前" + player_num, "即将发送播放请求")
    session.post(h5_url, data=data, proxies=proxys)
    session.close()


if __name__ == '__main__':
    sum = 0
    while True:
        try:
            video_url = "https://www.bilibili.com/video/BV1HN411K7ZB"
            print("bv号为:", video_url.split("/")[-1])
            sum = sum + 1
            proxys = get_tunnel_proxies()

            add_play_num(video_url, proxys)
            print(f"已经发送了{sum}次播放请求")
            print("-------------------------")
            time.sleep(0.5)
        except Exception as e:
            pass
