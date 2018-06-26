# -*- coding:utf-8 -*-
# CMS识别

import requests
import json
from hashlib import md5
import threading

# 通过目录识别
class cms_map:
    # 传入 url 和 最大线程数
    def __init__(self,url,threads=50):
        if 'http' not in url:
            url = 'http://' + url
        self.url = url.strip('/')
        self.threads = threads

    # 返回所有需要匹配的数据（目录+md5+re+cms_name） dict
    def get_all_data(self):
        cms_data_file = './cms_map/data.json'
        f = open(cms_data_file,'rb')
        cms_data = json.loads(f.read())
        f.close()
        return cms_data

    #   扫描主函数，启用多线程
    def main(self):
        # 定义一个变量来存放 cms 结果，方便参数传递
        # 返回一个 list  ==>  cms_result
        cms_result = []
        semaphore = threading.Semaphore(self.threads)
        all_data = self.get_all_data()
        for data in all_data:
            semaphore.acquire()
            url = self.url + data['url']
            if data['re']:
                thread = threading.Thread(target=self.scan_re,args=(url,data,semaphore,cms_result))
                thread.start()
            elif data['md5']:
                thread = threading.Thread(target=self.scan_md5,args=(url, data,semaphore,cms_result))
                thread.start()
        thread.join()
        return cms_result
    # 通过 re 匹配
    def scan_re(self,url,data,semaphore,cms_result):
        try:
            headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
            req = requests.get(url,headers=headers,timeout=3)
            if req.status_code == 200:
                content = req.text
                if str(data['re']) in content:
                    cms_result.append(data['name'])
                    #print ('re\t' + data['url'] + '\t' + data['name'])
            semaphore.release()
        except Exception as e:
            #print (e)
            semaphore.release()

    # 通过 md5 匹配
    def scan_md5(self,url,data,semaphore,cms_result):
        try:
            headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
            req = requests.get(url,headers=headers,timeout=3)
            if req.status_code == 200:
                content = req.content
                hash_md5 = self.md5_encrypt(content)
                if hash_md5 == data['md5']:
                    cms_result.append(data['name'])
                    #print ('md5\t' + data['url'] + '\t' + data['name'])
            semaphore.release()
        except Exception as e:
            #print (e)
            semaphore.release()

    # md5加密
    def md5_encrypt(self,encrypt_content):
        en = md5(encrypt_content)
        return en.hexdigest()

# 调用网上 api
class cms_api:
    def __init__(self,url):
        self.url = url.replace('http://','').replace('https://','').replace('/','')

    def main(self):
        url = 'http://whatweb.bugscaner.com/what/'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0','Referer':'http://whatweb.bugscaner.com/look/'}
        cocokies = {'saeut': 'CkMPHlqbqdBQWl9NBG+uAg=='}
        new_url = self.url.strip('/').replace('http://','').replace('https://','')
        data = {'url': new_url, 'hash': '0eca8914342fc63f5a2ef5246b7a3b14_7289fd8cf7f420f594ac165e475f1479'}
        content = json.loads(requests.post(url,headers=headers,data=data).text)
        return content['cms']
