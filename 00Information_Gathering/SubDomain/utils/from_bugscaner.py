
import requests
import json
from .config import *
import time

def from_bugscaner(target):
    subdomains=[]
    try:
        url = "http://tools.bugscaner.com//api/subdomain/"
        data={"inputurl":target}
        page = requests.post(url, timeout=timeout, headers=headers,data=data)
        result = json.loads(page.text)
        for subdomain in result['domain']:
            subdomain = subdomain.strip(" ")
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[ERROR]search subdomain from bugscaner error :%s" % e.args)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[INFO]restring...")
        from_bugscaner(target)
    return subdomains
