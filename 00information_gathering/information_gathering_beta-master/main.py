# -*- coding:utf-8 -*-
import sys
'''
功能表
  1. CMS识别  cms_map.py    2个类 main()  1个目录扫描  1个调用API   (√)
  2. WAF探测   GitHub         (×)
  3. Whois查询    whois_chinaz.py    1个类 main()  站长之家API (√)
  4. 子域名查询  subdomain_gathering.py  1个类 main()  百度搜索inurl:domain 查询 (√)
  5. CDN识别  cdn_finder.py (√)
  6. 常用端口扫描以及对应服务 port_scan.py 1个类 main() 调用 python-nmap库(√)
  7. whatweb扫描  网站脚本语言 IP 搭建平台  whatweb.py 1个类 main() 调用whatweb (√)
  8. 操作系统   whatweb 或者 nmap 可以探测    (√)
'''
# CMS 识别
from cms_map import cms_api
from cms_map import cms_map
# 站长之家信息收集
from whois_chinaz import whois
# 通过浏览器进行子域名查询
from subdomain_gathering import crew
# CDN探测
from cdn_finder import cdn_finder
# 端口扫描
from port_scan import port_scan
# whatweb 扫描
from whatweb import whatweb
# Robots 扫描
import Robots

def cms_scan(url):
    '''
    CMS 识别
    先调用 api 扫描
    无结果再遍历目录扫描
    '''
    def _api(url):
        instance = cms_api(url)
        cms = instance.main()
        return cms

    def _map(url):
        instance = cms_map(url, threads=1000)
        cms = instance.main()
        if len(cms) != 0:
            return cms[0]

    result = _api(url)
    if len(result) == 0:
        result = _map(url)
        if result == None:
            print ('[-] CMS识别失败')
        else:
            print (result)
    else:
        print (result)
def robots(url):
    result = Robots.view_robots(url)
    print (result)
def chinaz(url):
    '''
     站长之家信息收集
    method = 1 邮箱反查
    method = 2 注册人反查
    method = 3 电话反查
    '''
    instance = whois(url,method=None)
    results = instance.main()
    for info in results:
        print (info)
def sub_domain(url):
    '''
    通过浏览器进行子域名收集
    '''
    instance = crew(url)
    results = instance.main()
    for info in results:
        print (info)
def whatweb_gather(url):
    '''
    whatweb 信息收集
    '''
    instance = whatweb(url)
    results = instance.main()
    for info in results:
        try:
            print (info.decode('utf-8'))
        except:
            print (info)
def find_CDN(url):
    '''
    探测CDN
    '''
    instance = cdn_finder(url)
    result = instance.main()
    return result
def port_find(url):
    '''
    python-nmap 库进行端口扫描
    '''
    instance = port_scan(url)
    result = instance.main()
    for info in result:
        print (info)


def main():
    '''
    1.识别CMS
    2.Robots扫描
    3.站长之家查询
    4.子域名收集
    5.whatweb查询
    6.CDN查询
        6.1.端口扫描
    '''
    #url = 'http://www.discuz.net/'
    #url = 'http://parrotsec-china.org/'
    try:
        url = sys.argv[1]
        cms_scan(url)
        print ('\n\n')
        robots(url)
        print ('\n\n')
        chinaz(url)
        print ('\n\n')
        sub_domain(url)
        print ('\n\n')
        whatweb_gather(url)
        print ('\n\n')
        result = find_CDN(url)
        if result == ('[-] No CDN Found'):
            print (result)
            print ('\n\n')
            port_find(url)
        else:
            print (result)
    except:
        print ('Usage : python main.py <https://damit5.com/>')


if __name__ == '__main__':
    main()
