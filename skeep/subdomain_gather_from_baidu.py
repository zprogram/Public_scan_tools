# -*- coding:utf-8 -*-
# search from baidu.com
import sys

import requests
import re
import time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
# 定义全局变量
all_sub_domain = []

class crew:

    def __init__(self,url):
        self.url = url

    #第一页 page_num = 0，每一页+10
    def get_sub_domain(self,page_num=0):
        print u'[+] 正在爬取第 %d 页'%(page_num/10+1)
        print ('第{}页'.format(page_num/10))
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:%s'%(self.url,page_num,self.url)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        cookies = {'Cookie:BD_UPN': '12314753', ' PSINO': '3', ' BD_CK_SAM': '1', ' BDSVRTM': '0', ' H_PS_645EC': 'b578esKTCyumZeBSH1qhwLcj6MV3O1UW%2BYDCqiejMDwFlo8zftxCeMDl4fk', ' BD_HOME': '0', ' BIDUPSID': '3D18FDEB990518E39E456FB166607D79', ' H_PS_PSSID': '1467_18195_21108_17001_22159', ' BAIDUID': '671EE6A6C6D33975C07912AE59D606F4:FG=1', ' PSTM': '1518244624'}
        content = requests.get(url,headers=headers,cookies=cookies).text
        soup = BeautifulSoup(content,'lxml')
        one_page_urls = soup.findAll('a',class_="c-showurl")
        for one_url in one_page_urls:

            for i in one_url.strings:
                sub_domain = ""
                sub_domain += str(i)
                sub_domain = sub_domain.replace('https://', '').replace('http://', '')

                if  len(re.findall('/\w',sub_domain)) == 0 and sub_domain not in all_sub_domain:
                    sub_domain = sub_domain.replace('/', '')
                    print sub_domain
                    all_sub_domain.append(sub_domain)
                else:
                    pass

        if r'class="n">下一页' in content:
            new_page_num = page_num + 10
            time.sleep(1)
            self.get_sub_domain(new_page_num)

    def main(self):
        self.get_sub_domain(page_num=0)
        return all_sub_domain
