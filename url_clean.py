# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import os
from re import T
from time import process_time_ns
import requests
import dns.resolver

os.environ['no_proxy'] = '*'
requests.packages.urllib3.disable_warnings()

def isResolve(url):
    domain = url.split(":")[0]
    try:
        dns.resolver.resolve(domain,"A")
        return True
    except:
        return False

def isAlive(url):
    ret = -1
    t_url = "http://"+ url
    if(isResolve(url)):
        cookie_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}
        try:
            r = requests.get("http://"+url, headers=cookie_headers, timeout=5)
            ret = r.status_code
            if r.status_code != 200:
                r = requests.get("https://"+url, headers=cookie_headers, verify=False, timeout=5)
                t_url = "https://"+url
                ret = r.status_code
        except:
            pass
    return ret, t_url

def main():
    with open("t.txt", "r") as f:
        urls = f.readlines()

    n_urls = set()
    for url in urls:
        if url is NULL:
            continue
        # 去除多余字符，去重
        url = url.strip().replace(" ", "").replace("https://", "").replace("http://", "")
        n_urls.add(url)

    t_urls = set()
    for url in n_urls:
        ret,t_url = isAlive(url)
        ret = str(ret)
        if ret.startswith("2"):#Todo打印出来
            print(t_url)
            t_urls.add(t_url)
            pass
        elif ret.startswith("3"):#Todo 跟随跳转
            pass
        elif ret.startswith("5"):#Todo hosts碰撞，改refer头，改手机header，改XFF
            pass
        else:# 已经关站，就省略
            pass

    with open("result.txt","w") as ff:
        ff.writelines(t_urls) 


if __name__ == "__main__":
    main()