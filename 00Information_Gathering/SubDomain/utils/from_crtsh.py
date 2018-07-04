
import requests,time
from bs4 import BeautifulSoup
from .config import *
def from_crtsh(target):
    subdomains=[]
    try:
        url = "https://crt.sh/?q=%25." + target
        page = requests.get(url, timeout=timeout, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        td_list = soup.find_all("td")
            # print (td_list)
        for td in td_list:

            if (len(td.text) < 200):
                if "kuaishou.com" in td.text and "LIKE" not in td.text:
                    func = td.text
                    func_domain = func.replace("*.", "")
                    if func_domain not in subdomains:
                        subdomains.append(func_domain)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"[ERROR]search_subdomain_from_crtsh  error %s" % e.args)
        return []
    return subdomains

