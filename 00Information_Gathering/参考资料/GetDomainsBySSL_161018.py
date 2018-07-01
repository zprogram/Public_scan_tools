#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oritz'
__date__ = '2016/10'

__team__ = 'NSRC'

import os
import re
import json
import requests
import argparse
import lxml.html


class GetDomainsBySsl:

    # Todo: 对于 CDN 和 WWW 域名未处理

    def __init__(self, raw_domain):
        self.raw_domain = raw_domain
        self.TIMEOUT = 30
        self.x = []

    def get_json(self, x, token=''):  # 爬取下一页需要上一个请求中的 nextPageToken
        url = 'https://www.google.com/transparencyreport/jsonp/ct/search?domain=%s&incl_exp=true&incl_sub=true&c=data&token=%s' % (self.raw_domain, token)
        try:
            r = requests.get(url, timeout=self.TIMEOUT)
            if r.status_code == 200:
                data = r.text[23:-3]
                j = json.loads(data)
                x += j['results']

                if 'nextPageToken' in j:
                    self.get_json(x, j['nextPageToken'])  # 递归
                    return x

        except ConnectionError as e:
            print(e)

    def get_domains_from_google(self):  # 从 Google 获取域名  Todo: 多线程
        domains = set()
        results = self.get_json(self.x, '')
        if results is None:
            print('[!] There is no HTTPS domain for %s.' % self.raw_domain)
        else:
            for d in results:
                if 'firstDnsName' in d:
                    domains.add(d['firstDnsName'].replace("*.", ""))
                domains.add(d['subject'].replace("*.", ""))

        if self.raw_domain in domains:
            domains.remove(self.raw_domain)  # 排除用户输入的（根）域名
            if domains:
                print('[+] Number of Domains: %s\n%s' % (len(domains), domains))
            else:
                print('[!] It uses Wildcard Certificates for root domain.')

        return domains

    def get_domains_from_crt(self):  # 从 crt.sh 获取域名
        domains = set()
        url = "https://crt.sh/?Identity=%%.%s" % self.raw_domain
        try:
            r = requests.get(url,  timeout=self.TIMEOUT)
            if r.status_code == 200:
                doc = lxml.html.document_fromstring(r.text)
                td_info = doc.xpath("/html/body/table[2]/tr/td/table/tr/td[3]")
                for td in td_info:
                    if td.text:  # 排除空的情况
                        if "@" not in td.text and 'SingleDomain' not in td.text:  # 排除邮箱等情况
                            domain = td.text.split("=")[-1].replace("*.", "")
                            domains.add(domain)

        except ConnectionError as e:
            print(e)

        if self.raw_domain in domains:
            domains.remove(self.raw_domain)
            if domains:
                print('[+] Number of Domains: %s\n%s' % (len(domains), domains))
                return domains
            else:
                print('[!] There is no HTTPS domain for %s or it uses Wildcard Certificates for root domain.' % self.raw_domain)

    def get_domains_from_openssl(self):  # 使用 OpenSSL 的 SAN 获得域名，有命令注入风险
        domains = set()
        cmd = 'openssl s_client -showcerts -connect %s:443 < /dev/null 2>/dev/null | openssl x509 -text | grep -A 1 "Subject Alternative Name"' % self.raw_domain
        try:
            tmp = os.popen(cmd).readlines()
            data = re.split(r'DNS:', tmp[1].strip())
            for i in data:
                if i:
                    domains.add(i.replace(', ', '').replace('*.', ''))

            if self.raw_domain in domains:
                domains.remove(self.raw_domain)
                if domains:
                    print('[+] Number of Domains: %s\n%s' % (len(domains), domains))
                else:
                    print('[!] Its Subject Alternative Name is exactly itself.')

        except Exception:
            print('[!] You have no OpenSSL or there is no HTTPS domain for %s.' % self.raw_domain)

        return domains

    def get_domains(self):
        print('[-] Get Domains from OpenSSL ...')
        openssl_domains = self.get_domains_from_openssl()
        print('[-] Get Domains from crt.sh ...')
        crt_domains = self.get_domains_from_crt()
        print('[-] Get Domains from Google, it will be a little slow ...')
        google_domains = self.get_domains_from_google()

        if crt_domains or google_domains or openssl_domains:
            total_domains = (crt_domains | google_domains | openssl_domains)
            print('[√] Total Domains: %s\n%s' % (len(total_domains), total_domains))
        else:
            print('[X] Oops, there is nothing!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get Domains by SSL")
    parser.add_argument("domain", help="The domain that you want to test. e.g. jd.com")
    raw_domain = parser.parse_args().domain
    GetDomainsBySsl(raw_domain).get_domains()