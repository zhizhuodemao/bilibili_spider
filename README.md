# bilibili_spider
这个项目是为了bilibili刷点击量使用
# 前言
 该教程由Mr.chen所作 仅为自己学习使用 使用者仅为合法合规的研究使用,如有拿去商业行为导致b站利益受损,与本人毫无关系
 
 首先 我们要做的内容是刷播放量 我们应当先了解以下内容
 
 1.只有点击播放按钮才算播放量 只加载视频不点播放不算播放量
 
 2.点击播放之后应该是发送了一个请求 该请求后台收到之后可以会把数据库中播放量加1 我们要做的就是解析这个请求 发这个请求
 
 3.每个视频应该是点击的那一瞬间发送的请求 并且只发送一次请求 因为播放量只增加一次
 
 4.请求应该是异步的 xhr请求
 
 所以 我们应该在页面完全加载之后,视频还没开始播放的时候,点击播放按钮,看看发送了什么请求
 
 同时  我们应该选用一个之前没有登陆过b站的浏览器 最好是全新的浏览器来观察 避免之前cookie的影响
 
 现在 我们启用谷歌浏览器的无痕模式 模拟全新登录 让页面停留在加载完成之后 还没播放视频的界面
 
![1](https://user-images.githubusercontent.com/47770924/227782848-59f2264c-37f8-4aaa-97ba-22cfd197373d.png)

应当注意的是 这个自动开播的按钮我们需要关闭才能完成操作 关闭之后刷新页面 理论上来说现在可能已经存在上次加载的cookie了

但是在默认的情况下又只能自动播放 所以我们最终使用火狐浏览器做开始的判别 后来再用谷歌 因为火狐浏览器有阻止播放视频的功能

![2](https://user-images.githubusercontent.com/47770924/227782926-54259e18-aeb4-419a-9c7b-02a6a3ffd1e4.png)

我们应该先打开调试工具 再访问这个页面

![3](https://user-images.githubusercontent.com/47770924/227783086-84cd538f-3b16-4ef2-a8e2-21795d9f3532.png)
调出抓包工具 开始调试
![4](https://user-images.githubusercontent.com/47770924/227783115-9d7e989c-a9d5-48f1-82a4-03a4dbeda097.png)
对于网页来说,往往我们的第一个请求都是返回页面的请求 这个请求一般可以不携带cookie 如下图 很常见的请求头 我们接下来看看响应
![5](https://user-images.githubusercontent.com/47770924/227783140-6fe1b95f-d2f8-49f6-916b-b063c632d8c3.png)
我们发现这个请求再响应的时候添加了两个cookie 一个叫b_nut 一个叫bu_vid3
![6](https://user-images.githubusercontent.com/47770924/227783146-46c9751a-63b4-4898-92f5-e9710249e633.png)
这里应当保持我们的浏览器之前没有任何cookie 在火狐浏览器中设置每次退出时清除所有cookie 不然就无法达到我这个效果
![7](https://user-images.githubusercontent.com/47770924/227783161-e3c55873-7867-4aa5-8a19-efe634ba4318.png)
如果我尝试刷新这个页面 这个请求就会携带很多cookie了 该返回的cookie也不再返回 不利于我们分析 如下图
![8](https://user-images.githubusercontent.com/47770924/227783168-be2bc2ad-560e-4a61-9fa5-ddfc64f487b0.png)
因为第一个请求往往是页面请求 非常重要 我们才去分析 后面的请求不再一一分析
我们前边说过要找到点击播放按钮之后的那个请求 我们先清除现在的请求 避免影响判断
![9](https://user-images.githubusercontent.com/47770924/227783180-a11d7e70-95d3-4c84-8006-fa28fbe3baaf.png)
然后点击播放按钮 看看多了什么请求 这里注意 就算我们不点击播放按钮 也会有请求发送 不要被影响了可以一直清除

我点击之后立刻点击暂停 理论上视频的播放量已经加一了 请求已经发出去了 如下这几个请求
![10](https://user-images.githubusercontent.com/47770924/227783189-c83e26de-329f-4cc4-b7af-02f849593bf4.png)
之前我们分析过了 点击播放时会发请求 但是应该只会发一个请求 所以如果有多个请求 先给排除

其次 如果请求之前有发送过 现在又发送 显然也要排除

最后这个请求只发送一次 如果之后会继续发送同样的请求 也需要排除

这里需要注意的是 我们看请求一不一样只看?前边的部分 问号后边的部分不同不影响该请求的功能 这个是前端的基础知识

因此排除now heartbeat total web等请求 只剩一个h5请求

我们能确定吗？显然也不是百分百确定 这个时候我们也没其他办法 可以网上搜索看看其他人的方法 看看跟我们的结论一不一样 如果没有案例之前

那就先实现这个最可能的请求 如果没作用我们再去想别的办法

现在问题就转化为分析并实现H5这个请求 点击一次播放发送一次h5请求,增加一次播放量 如果我们直接发送h5请求 是不是也能增加播放量

首先这个H5请求是POST请求 对于post请求 需要分析其请求头和请求体

对于请求头一般cookie和token等字样比较关键 token也可能包含在cookie中 需要具体分析

对于请求体 我们需要看看请求体是否加密 如果加密需要找到加密方法 如果未加密 我们尝试分析请求体中的各个参数

非常幸运的是 我们再请求头中发现只有cookie参数需要解密 请求体也并未加密

![11](https://user-images.githubusercontent.com/47770924/227783473-89d27199-5214-4767-ba5c-128600be0525.png)![12](https://user-images.githubusercontent.com/47770924/227783477-2f93c201-3419-498e-8d80-0064c8fde1f3.png)

我们来看请求体和cookie 发现请求体数据似乎简单一些 我们先来分析请求体

这时候 我们先看看请求体中的参数会不会变化 如果不会变化 直接拿来用就是了 如果会变化 再进行下一步分析

先来点击其他的页面 查看h5请求 我们访问了两个页面 看到大部分的参数其实都没变化 有变化的是aid cid 以及ftime stime from_spmid

注意:刷新这个视频 aid cid不变

from_spmid可以看作没变化 因为之后都不会再变化 这个参数我们通过英文也能看出是这个请求从哪里来的 这里显示从推荐视频中过来的

ftime,stime如果你看网页多了就知道多半这两个东西都是时间戳 后端一般不会对时间戳做校验 我们随便拿一组就可以 我们可以通过简单的js代码验证

![13](https://user-images.githubusercontent.com/47770924/227783532-bc5eba81-759b-410b-81ed-4beb6f26efa6.png)![14](https://user-images.githubusercontent.com/47770924/227783539-b30f20f5-2659-4650-9581-5b0562ac7f10.png)![aa](https://user-images.githubusercontent.com/47770924/227783563-f1963f60-6dcc-41a9-906b-117be2ce5351.png)

因此 我们需要解决的就是aid 和cid

这里我们继续分析我们是点击鼠标发送的请求 让播放量加一 如果是我们发送请求 那么需要发送什么数据

是不是只要这个视频是哪个视频就够了 那么假设aid cid跟视频有关 那么这个参数是这个请求独占的吗？可能不是 毕竟这个页面加载出来视频是第一步 在这个请求发送之前有很多个请求都出现了 如果这两个参数代表视频信息 没理由会为了这个请求单独生成这么一组参数

是不是可以猜测 这个请求用到的aid cid是之前生成的 只是现在拿过来用?

以上只是分析 具体在做的时候也可能是请求在发送的时候js代码生成的参数 被封装到这个请求中发出去

其实在这里基本可以认为是以前请求生成的 这里直接拿到 因为参数没加密 应该是某次请求返回之后 保存在js的全局变量中 这里拿出来调用

我们尝试以aid搜索 发现第一次出现在请求中是v2请求 并且v2请求和现在一样也是拿过来用 这说明在v2之前就生成了这两个id

![15](https://user-images.githubusercontent.com/47770924/227783645-9447fd03-858f-4574-b32f-9401508998f0.png)

v2已经是比较靠前的请求了 前边值得一提的请求只剩我们最开始的页面请求了 那说明很可能是加载页面之后这两个id就返回了

为了验证 我们再次搜索所有的资源 果然发现所有的请求都是url和path出现 但是首页请求是出现在返回html中 我们在html中再次搜索

果然发现aid和cid都藏在embedPlayer这个变量里

![16](https://user-images.githubusercontent.com/47770924/227783698-6429ebda-2976-4af6-98bd-8bedf06efa1c.png)

接下来的事情就简单了 发送首页请求 在响应中用正则表达式拿到aid和cid

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
    

至此 我们的请求体中数据算是处理完成 开始处理请求头 再次用无痕模式打开视频 需要处理的cookie如图所示

![17](https://user-images.githubusercontent.com/47770924/227783770-47ee612f-2744-4086-9abd-fb8b40e807bc.png)

这里有个小技巧 可能不是所有的cookie都是必要的 我们可以试试在抓包工具中去掉某个cookie看看请求能不能正常发送

这里我们尝试清除所有的cookie 请求依然正常发送 正常返回 那么是不是不需要cookie呢?我们尝试写代码发现 虽然正常返回 但是播放数不会增加

这里有个小技巧 可能不是所有的cookie都是必要的 我们可以试试在抓包工具中去掉某个cookie看看请求能不能正常发送

这里我们尝试清除所有的cookie 请求依然正常发送 正常返回 那么是不是不需要cookie呢?我们尝试写代码发现 虽然正常返回 但是播放数不会增加

    import requests
    from lxml import etree
    import time
    
    url = "https://api.bilibili.com/x/click-interface/click/web/h5"
    first_url = "https://www.bilibili.com/video/BV1wX4y1o7dB"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    data = {
        "aid": 354029066,
        "cid": 1070352129,
        "part": 1,
        "lv": 0,
        "ftime": 1679738091,
        "stime": 1679738090,
        "type": 3,
        "sub_type": 0,
        "refer_url": "",
        "spmid": "333.788.0.0,",
        "from_spmid": "",
        "csrf": ""
    }
    sum = 0
    while True:
        page_text = requests.get(first_url, headers).text
        html = etree.HTML(page_text)
        player_num = html.xpath('//*[@id="viewbox_report"]/div/div/span[1]/@title')[0]
        print(player_num, "即将发送播放请求")
        res = requests.post(url=url, data=data, headers=headers)
        sum = sum + 1
        print(f"已经发送了{sum}次播放请求")
        time.sleep(1)

![18](https://user-images.githubusercontent.com/47770924/227783907-158df90e-2629-4129-9d92-3a58531afaab.png)
    
现在有两种可能 一个是这个请求压根不是增加播放的请求 这种可能几乎为0 通过js逆向我已经几乎可以确定该请求就是增加播放量的请求

还有一种可能就是缺少cookie 现在只有先解码cookie的生成了

![19](https://user-images.githubusercontent.com/47770924/227784103-8abefc7b-3be1-49b7-839b-c6d2275c8532.png)

之前我们发现这个请求再响应的时候添加了两个cookie 一个叫b_nut 一个叫bu_vid3

所以这两个cookie不需要我们处理 依然是之前的流程 刷新页面 换其他的视频看看cookie是否有变化 没变化的就不管 直接复制

我们发现 在所有需要处理的cookie中 buvid_fp和CURRENT_FNVAL刷新页面不改变 可以复制

改变的有b_lsid,_uuid,sid,buvid4

这几个id的来源有两种可能 一是之前页面返回设置 二是之前某个请求发送时js生成

先看之前的请求有没有生成

我们发现v2请求有生成sid 剩下b_lsid,_uuid,buvid4需要处理
![20](https://user-images.githubusercontent.com/47770924/227784235-bcd101e8-0b33-4721-8317-48ca9739f070.png)

最早在web请求时就已经携带 说明生成cookie在此之前就生成了
![21](https://user-images.githubusercontent.com/47770924/227784243-b10eaf1d-ec85-493d-abbf-41bba5594084.png)

我们只看看cookie是怎么加密的 因此尝试搜索这几个id

先搜b_lsid 看到在reporter.js和log-reporter.js中出现 随便进一个 比如log-reporter.js 搜索b_lsid

![22](https://user-images.githubusercontent.com/47770924/227784280-b30b7a6f-a96f-410e-bf26-dc03e90464fc.png)

发现出现了setCookie这个函数 那极有可能就是在这里设置的b_lsid

进入js文件 打断点看看 发现断点始终不触发 这是正常的 因为一般只有在第一次请求没有这个cookie时才会设置cookie 因此我们尝试清除cookie再次刷新


![23](https://user-images.githubusercontent.com/47770924/227784308-64a01ecc-0961-4a62-9c45-d6eb563748a5.png)

在这里我们可以看到b_lsid的生成

显然e是时间字典

Object(f.b)指的是f.b函数 点进去如图所示
![24](https://user-images.githubusercontent.com/47770924/227784349-fe875d5f-e79e-4ddf-9cb5-3a4af6bdddab.png)
该函数只是把传进来的参数e向上取整 然后转成16进制最后转成大写
![25](https://user-images.githubusercontent.com/47770924/227784389-2a5725cd-2b15-4149-a222-33ff8d0fe54e.png)
再看f.c 点进去
显然这里是把8传入这个函数 o依然是上面的操作 返回s(t,e),s也不复杂 看看传入的参数有没有t的长度 没有 差多少就补0
进入setCookie函数中 发现就是普通的拼接cookie的操作 没有对以上的t进行改变 所以 我们直接用pyexejs结合nodejs来实现b_lsid的生成
    function get_b_lsid() {
        t = b(new Date().getTime()), t = "".concat(Object(c)(8), "_").concat(t);
        return t
    }
    
    function b(e) {
        return Math.ceil(e).toString(16).toUpperCase()
    }
    
    c = function (e) {
        for (var t = "", n = 0; n < e; n++)
            t += o(16 * Math.random());
        return s(t, e)
    }
    s = function (e, t) {
        var n = "";
        if (e.length < t)
            for (var r = 0; r < t - e.length; r++)
                n += "0";
        return n + e
    }
    o = function (e) {
        return Math.ceil(e).toString(16).toUpperCase()
    }
    var b_lsid = get_b_lsid()
    console.log(b_lsid)

现在看_uuid 我们发现都在一个js文件里

同样的方法 我们找到_uuid生成的函数为

var get_uuid = function () {
    var e = a(8)
        , t = a(4)
        , n = a(4)
        , r = a(4)
        , o = a(12)
        , i = (new Date).getTime();
    return e + "-" + t + "-" + n + "-" + r + "-" + o + s((i % 1e5).toString(), 5) + "infoc"
}
    ,a = function (e) {
    for (var t = "", n = 0; n < e; n++)
        t += o(16 * Math.random());
    return s(t, e)
}
console.log(get_uuid())

再来看bvid4通过搜索找到setCookie

![26](https://user-images.githubusercontent.com/47770924/227784516-367c8ad3-8fb6-4f76-bd03-b98deab04f82.png)

该请求需要的的cookie我们都解密完成了 刚好可以拿到buvid4

![27](https://user-images.githubusercontent.com/47770924/227784609-c1ce9362-4e8b-46ee-a4d3-ff4d351dea21.png)
至此 所有cookie解密完成

下面的流程是先发送首页请求,用session发送,然后通过我们的算法组装好cookie,发送spi请求,拿到返回的buvid值,最终发送增加播放量的请求,查看效果

代码如下

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
        proxy_host = "xxx"
        proxy_username = "xxxx"
        proxy_pwd = "xxx"
    
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
    
    

后来发现 确实没有cookie也能发请求 之前不能增加播放量是因为没有使用代理 只能增加一次播放量 使用代理之后就没问题了 也就是说cookie不需要了

写到这里感觉怀疑人生了。。。。

    import requests
    from lxml import etree
    import time
    import re
    import json
    import random
    
    
    def get_tunnel_proxies():
        proxy_host = "xxxx"
        proxy_username = "xxx"
        proxy_pwd = "xxx"
    
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
    



