# -*- coding:utf-8 -*-
# search from baidu.com

import requests
import re
from bs4 import BeautifulSoup

# 定义全局变量
all_sub_domain = []

class crew:
    def __init__(self,url):
        self.url = self.extract_url(url)

    # 提取域名
    def extract_url(self,url):
        url = url.replace('https://','').replace('http://','').replace('/','')
        if 'edu' in url:
            if len(url.split('.')) > 3:
                url = url.split('.')[-3] + '.' + url.split('.')[-2] + '.' + url.split('.')[-1]
            return url
        elif len(url.split('.')) > 2:
            url = url.split('.')[-2] + '.' + url.split('.')[-1]
        return url

    #第一页 page_num = 0，每一页+10
    def get_sub_domain(self,page_num=0):
        #print u'[+] 正在爬取第 %d 页'%(page_num/10+1)
        #print ('第{}页'.format(page_num/10))
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:%s'%(self.url,page_num,self.url)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        cookies = {'Cookie:BD_UPN': '12314753', ' PSINO': '3', ' BD_CK_SAM': '1', ' BDSVRTM': '0', ' H_PS_645EC': 'b578esKTCyumZeBSH1qhwLcj6MV3O1UW%2BYDCqiejMDwFlo8zftxCeMDl4fk', ' BD_HOME': '0', ' BIDUPSID': '3D18FDEB990518E39E456FB166607D79', ' H_PS_PSSID': '1467_18195_21108_17001_22159', ' BAIDUID': '671EE6A6C6D33975C07912AE59D606F4:FG=1', ' PSTM': '1518244624'}
        content = requests.get(url,headers=headers,cookies=cookies).text
        soup = BeautifulSoup(content,'lxml')
        one_page_urls = soup.findAll('a',class_="c-showurl")    # 匹配到所有的含有子域名的标签
        for one_url in one_page_urls:
            sub_domain = ''
            for i in one_url.strings:   # 提取标签中的内容
                try:
                    sub_domain += str(i)
                except:
                    pass
            # 子域名和存活性检测并且判断是否为子域名
            # 不存在list里面     存活      不是目录
            if sub_domain not in all_sub_domain and self.is_alive('http://' + sub_domain) and len(re.findall('/\w',sub_domain)) == 0:
                all_sub_domain.append(sub_domain)
                print (sub_domain)
        if 'class="n">下一页' in content:
            new_page_num = page_num + 10
            self.get_sub_domain(new_page_num)

    # 存活性检测
    def is_alive(self,url):
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            if requests.get(url,headers=headers,timeout=1).status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def main(self):
        self.get_sub_domain(page_num=0)
        return all_sub_domain
