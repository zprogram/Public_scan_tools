#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#子域名扫描框架
#

import requests
from termcolor import colored
from bs4 import BeautifulSoup
import threading
import time
import sys
import json
import re
import os
import logging
import random
import base64
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

#MY_PROXY = { "http":"127.0.0.1:8080","https":"127.0.0.1:8080"}
MY_PROXY = {}
USER_AGENTS=[
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)']

def search_subdomain_from_virustotal(target):
    #  功能： 传入一个顶级域名，返回子域名列表，利用的网站是virustotal
    #
    #
    #  效果比较好

    #
    #需要确认一下crt.sh的功能
    #
    #
    print("Start search_subdomain_from_virustotal")
    domain_result = []
    url = "https://www.virustotal.com/ui/domains/"+target+"/subdomains?limit=30"

    try:
        resp = requests.get(url, timeout=10, proxies=MY_PROXY, headers={"User-Agent": random.choice(USER_AGENTS)})
        result = json.loads(resp.text)
        print (result)
    except:

        print("search_subdomain_from_virustotal connect error")
        return []
    print(result["links"])

    while "next" in result["links"]:
        try:
            resp = requests.get(result["links"]["next"], timeout=10, proxies=MY_PROXY,headers={"User-Agent": random.choice(USER_AGENTS)})
            result = json.loads(resp.text)
            for i in range(len(result["data"])):
                domain_result.append(result["data"][i]["id"])
            time.sleep(1)

        except:
            continue
    print("Complete search_cert_from_crt",'green')
    return domain_result


    '''
        while result["links"].has_key("next"):
        try:
            resp = requests.get(result["links"]["next"], timeout=10, proxies=MY_PROXY, headers={"User-Agent": random.choice(USER_AGENTS)})
            result = json.loads(resp.text)
            for i in range(len(result["data"])):
                print (i)
                domain_result.append(result["data"][i]["id"])
            time.sleep(1)
        except:

            continue
    print("Complete search_cert_from_crt",'green')
    return domain_result
    
    '''

    
    




def search_cert_from_crt(target):
    #  功能： 传入一个顶级域名，返回子域名列表，利用的网站是 crt.sh
    #
    #
    #  bug：返回的结果如下
    #['57673ceefad3259fddc47a241c74ae58319649b692d5760e505811998b186cbe']
    #['1a40d5f60f408df4a0740e8f1dd0d94fbb3427b363fd0fa3b8879221a7a5c76f']
    #['c165f38dc2362c33eeae401ff1e36bfdfa72fd251fccf4ff56bcdbb057fe427b']
    #['83e8d21a85eb4555f6e9bb186232f20e9bf53530bb0245d1984f952927041f2b']
    #['1e4df000f5e57f35d97191dd6af268d7ef9861f6f6b458acdef269b83844f1ef']
    #['d444fa7ef4c497c558cb8468510cf89dc154693acca0654e59cc8985cba851a1']
    #['534edf5b354cf0754074d1c6855dc1ec36a797ee225ce961ab15577e62efac63']
    #['b2e0a402fc33e26d508aa43c1e1f7ef01254a2de6fc9b1942b0da9804b2277c6']
    #['7d3eba5fe60745796470d22ded9d0266bf42fc41b2206e8d20b2ddc9db25c4fe']
    #['483ae70b7cf259bf9d179984b3221a2211834e5eb3d00de7cd717540fcf5393c']
    #
    #需要确认一下crt.sh的功能
    #
    #
    print("Start search_cert_from_crt")
    crt_api = "https://crt.sh/?q="
    cert_result = []
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        resp = requests.get("https://crt.sh/?q=baidu.com", headers={'Connection':'close',"User-Agent": random.choice(USER_AGENTS)})
    except:
        print("search_cert_from_crt connect error")
        return []
    id_result = re.findall("href=\"\?id=(.*?)\"",resp.text)
    for i in id_result:
        try:
            resp = requests.get("https://crt.sh/?id="+i, headers={'Connection':'close'})
            result = re.findall("\"//censys.io/certificates/(.*?)\"",resp.text)
            print(result)
            #cert_result.append(result[0])
        except:
            continue
    cert_result = list(set(cert_result))
    print("Complete search_cert_from_crt")
    return cert_result



def scan_subdamin_funcs(target):
    cert_list = search_cert_from_crt(target)
    print (cert_list)
    '''
    domains.extend(search_subdomain_from_virustotal(target))
    domains.extend(search_subdomain_from_threatcrowd(target))
    domains.extend(search_subdomain_from_findsubdomain(target))
    '''
    










if __name__ == '__main__':
    global domains
    top_damain="qq.com"
    #scan_subdamin_funcs(top_damain) 测试完成
    #print(search_subdomain_from_virustotal(top_damain))