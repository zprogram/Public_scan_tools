#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#子域名扫描框架
#
from subdomain_gather_from_baidu import crew
import json
import random
import re

from bs4 import BeautifulSoup
import time
import requests
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
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

def search_subdomain_from_crt(target):
    #  功能： 传入一个顶级域名，返回子域名列表，利用的网站是 crt.sh
    #
    #
    print("Start search_cert_from_crt")
    crt_api = "https://crt.sh/?q=%25."
    cert_result = []
    try:
        print crt_api+target
        resp = requests.get(crt_api+target, verify=False)
        time.sleep(10)
    except Exception as e:

        print(e.message)
        return []


    soup=BeautifulSoup(resp,"lxml")
    tr_list=soup.select("tr")
    print tr_list
    cert_result = list(set(cert_result))
    print("Complete search_cert_from_crt")
    return cert_result

def search_subdomain_from_threatcrowd(target):
    print("Start search_subdomain_from_threatcrowd")
    try:
        url = "https://www.threatcrowd.org/graphHtml.php?domain="+target
        resp = requests.get(url, timeout=10, headers={"Host":"www.threatcrowd.org","User-Agent": random.choice(USER_AGENTS),"Cookie":"__cfduid=da6b5b8144bfd70de8c3eb0aa7f0884661530196391; cf_clearance=e7a44a7fc942444b06a7817a5e02a5527adefd4b-1530196396-14400; _ga=GA1.2.736277610.1530196427; _gid=GA1.2.503529654.1530196427; __ar_v4=4OCRKBF4JJENXICP676FJT%3A20180628%3A2%7CKDBRCBINVREGNJUXIQKBDP%3A20180628%3A2%7CPIUCN4PSYRCCHBHOGPVN5Q%3A20180628%3A2"})
        requests.adapters.DEFAULT_RETRIES = 5
        print resp.status_code
        domain_result = re.findall("'>([^>]*?\."+target+")</a>",resp.text)
        print domain_result
        print("Complete search_subdomain_from_threatcrowd")
        return domain_result
    except Exception,e:
        print e
        return []

def search_subdomain_from_findsubdomain(target):
    print("Start search_subdomain_from_findsubdomain",'green')
    try:
        url = "https://findsubdomains.com/subdomains-of/"+target
        resp = requests.get(url, timeout=10, proxies=MY_PROXY, headers={"User-Agent": random.choice(USER_AGENTS)})
        domain_result = re.findall("'([^<>\"/]*?\."+target+")",resp.text)
        print("Complete search_subdomain_from_findsubdomain",'green')
        return domain_result
    except Exception,e:
        print("search_subdomain_from_findsubdomain connect error",'red')
        return []

def sub_domain(url):
    '''
    通过浏览器进行子域名收集
    '''
    instance = crew(url)
    results = instance.main()
    for info in results:
        print (info)

if __name__ == '__main__':


    global domains
    top_damain="qq.com"
    #print(search_subdomain_from_crt(top_damain))
    #print(search_subdomain_from_virustotal(top_damain))
    #print(search_subdomain_from_threatcrowd(top_damain))
    sub_domain(top_damain)