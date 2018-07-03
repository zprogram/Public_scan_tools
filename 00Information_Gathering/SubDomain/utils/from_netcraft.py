
import time
import requests
from bs4 import BeautifulSoup
from .config import *

def from_netcraft(target):
    subdomains=[]
    try:
        url = "http://searchdns.netcraft.com/?restriction=site+contains&host="+target
        page = requests.get(url, timeout=timeout, headers=headers)
        soup=BeautifulSoup(page.text,"html.parser")
        url_list=soup.find_all("a")
        for sub_url in url_list:
            if target in sub_url['href'] and target in sub_url.text:
                subdomain=sub_url.text
                subdomain = subdomain.strip(" ")
                if subdomain not in subdomains:
                    subdomains.append(subdomain)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[ERROR]search subdomain from netcraft error :%s" % e.args)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[INFO]restring...")
        from_netcraft(target)

    return subdomains