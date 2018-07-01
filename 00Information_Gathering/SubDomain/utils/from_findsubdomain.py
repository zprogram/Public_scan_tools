import requests
import json
import random
from .config import *
import time
import re

def from_findsubdomain(target):
    subdomains=[]

    try:
        url = "https://findsubdomains.com/subdomains-of/"+target
        resp = requests.get(url, timeout=timeout, headers=headers)
        domain_result = re.findall("'([^<>\"/]*?\."+target+")",resp.text)
        for subdomain in domain_result:
            subdomain=subdomain.strip(" ")
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[ERROR]search_subdomain_from_findsubdomain  error %s" % e.args)
        print("retrying ....")
        time.sleep(5)
        from_findsubdomain(target)
    return subdomains