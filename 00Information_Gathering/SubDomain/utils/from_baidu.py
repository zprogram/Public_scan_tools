#!/usr/bin/python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import time


def from_baidu(target,page_num):
    try:
        subdomains=[]
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:%s'%(target,page_num,target)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        cookies = {'Cookie:BD_UPN': '12314753', ' PSINO': '3', ' BD_CK_SAM': '1', ' BDSVRTM': '0', ' H_PS_645EC': 'b578esKTCyumZeBSH1qhwLcj6MV3O1UW%2BYDCqiejMDwFlo8zftxCeMDl4fk', ' BD_HOME': '0', ' BIDUPSID': '3D18FDEB990518E39E456FB166607D79', ' H_PS_PSSID': '1467_18195_21108_17001_22159', ' BAIDUID': '671EE6A6C6D33975C07912AE59D606F4:FG=1', ' PSTM': '1518244624'}
        content = requests.get(url,timeout=30,headers=headers,cookies=cookies).text
        soup = BeautifulSoup(content,"html.parser")
        one_page_urls = soup.findAll('a',class_="c-showurl")
        for one_url in one_page_urls:
            for i in one_url.strings:
                i=i.encode("utf-8")
                sub_domain = ""
                sub_domain += str(i)
                sub_domain = sub_domain.replace('https://', '').replace('http://', '')
    
                if  len(re.findall('/\w',sub_domain)) == 0 and sub_domain not in subdomains:
                    if "?" not in sub_domain:
                        if "#" not in sub_domain:
                            sub_domain = sub_domain.replace('/', '')
                            subdomains.append(sub_domain)
                else:
                    pass
    
        if u'class="n">下一页' in content:
            new_page_num = page_num + 10
            time.sleep(1)
            from_baidu(target,new_page_num)
            
            
   
    except Exception as e:
        print(e.args)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[INFO]restring...")
        from_baidu(target, 0)

    return subdomains