# -*- coding:utf-8 -*-
import requests
import json
import socket
import re
import whois

# 定义全局变量 CDN列表
CDN = {
    'Cloudflare': 'Cloudflare - https://www.cloudflare.com',
    'Incapsula': 'Incapsula - https://www.incapsula.com/',
    'Cloudfront': 'Cloudfront - https://aws.amazon.com/cloudfront/',
    'Akamai': 'Akamai - https://akamai.com',
    'Airee': 'Airee - https://airee.international',
    'CacheFly': 'CacheFly - https://www.cachefly.com/',
    'EdgeCast': 'EdgeCast - https://verizondigitalmedia.com',
    'MaxCDN': 'MaxCDN - https://www.maxcdn.com/',
    'Beluga': 'BelugaCDN - https://belugacdn.com',
    'Limelight': 'Limelight -  https://www.limelight.com',
    'Fastly': 'Fastly - https://www.fastly.com/',
    'Myracloud': 'Myra - https://myracloud.com',
    'msecnd.ne': 'Microsoft Azure - https://azure.microsoft.com/en-us/services/cdn/',
    'Clever-cloud': 'Clever Cloud - https://www.clever-cloud.com/'
}

class cdn_finder:

    def __init__(self,url):
        if 'http' not in url:
            url = 'http://' + url
        self.url = url

    def ErrorServerDetection(self):
        '''
        服务器错误信息检测

        直接访问IP时CDN会显示错误信息，页面中会显示CDN服务商名称
        '''
        host = re.sub('https://|/|http://','',self.url)
        ip = socket.gethostbyname(host)
        try:
            content = requests.get('http://' + ip,timeout=10).text
        except:
            content = ''
        for keyword,description in CDN.items():
            if keyword.lower() in str(content).lower():
                return description
        return None

    def WhoisDetection(self):
        '''
        CDN会修改服务器名称，nserver等信息并且在whois结果中显示
        '''
        content = whois.whois(self.url)
        for keyword,description in CDN.items():
            if keyword.lower() in str(content).lower():
                return description
        return None

    def HTTPHeaderDetection(self):
        '''
        一些CDN在HTTP头中会显示信息
        '''
        try:
            headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
            headers = requests.get(url,headers=headers).headers
            for keyword,description in CDN.items():
                if keyword.lower() in str(headers).lower():
                    return description
            return None
        except:
            return None

    def main(self):
        ErrorServerDetection = self.ErrorServerDetection()
        if ErrorServerDetection != None:
            return ErrorServerDetection

        WhoisDetection = self.WhoisDetection()
        if WhoisDetection != None:
            return WhoisDetection

        HTTPHeaderDetection = self.HTTPHeaderDetection()
        if HTTPHeaderDetection != None:
            return HTTPHeaderDetection

        return '[-] No CDN Found'
