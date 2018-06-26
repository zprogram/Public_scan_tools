# -*- coding:utf-8 -*-
import requests
import re

class whatweb:
    '''
    自动使用 whatweb 扫描，并返回结果，返回格式为 generate
    '''
    def __init__(self,url):
        self.url = re.sub('http://|https://|/','',url)

    def whatweb(self):
        '''
        通过whatweb扫描获取内容
        '''
        url = 'https://www.whatweb.net/whatweb.php'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0','Referer':'https://www.whatweb.net/'}
        data = {'target': self.url}
        return requests.post(url,headers=headers,data=data).text

    def parse_content(self):
        '''
        解析 whatweb 识别出来的内容
        '''
        content = self.whatweb()
        content = content.replace(',','').replace('\n','').replace('][',' ')
        single_information = content.split(']')    #每一条信息
        for single in single_information:
            try:
                yield (single.split('[',1)[0] + ' : ' + single.split('[',1)[1]).strip(' ')
            except:
                yield single

    def main(self):
        '''
        主函数，启动函数
        '''
        results = self.parse_content()
        results = [result for result in results]
        return results
