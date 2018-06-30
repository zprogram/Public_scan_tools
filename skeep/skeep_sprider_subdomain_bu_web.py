import json
import random
import re

from bs4 import BeautifulSoup
import time
import requests
import random
from urllib import request

subdomains=[]
http_proxy=[{"http":"117.146.19.161:3128"},{"http":"140.205.222.3:80"},{"http":"115.84.179.249:7777"},{"http":"111.13.61.60:3128"}]
USER_AGENTS=[
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)']

def from_threatcrowd(target):
    print("Start search_subdomain_from_threatcrowd")
    try:
        url = "https://www.threatcrowd.org/graphHtml.php?domain="+target
        resp1 = requests.get("http://www.threatcrowd.org/searchApi/v2/domain/report/", data={"domain": "aoldaily.com"},timeout=30, headers={"Host":"www.threatcrowd.org","User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36"})
        print(resp1.status_code)
        time.sleep(10)
        resp2 = requests.get(url, timeout=30, headers={"Host":"www.threatcrowd.org","User-Agent": random.choice(USER_AGENTS)})

        #requests.adapters.DEFAULT_RETRIES = 5
        print (resp2.status_code)
        print(resp2.content)
        domain_result = re.findall("'>([^>]*?\."+target+")</a>",resp2.text)
        print (domain_result)
        print("Complete search_subdomain_from_threatcrowd")


    except Exception as e:

        print("search_subdomain_from_threatcrowd error %s" % e.args)

        print("retrying ....")

        time.sleep(5)

        #from_findsubdomain(target)

def from_findsubdomain(target):
    print("Start search_subdomain_from_findsubdomain")
    try:
        url = "https://findsubdomains.com/subdomains-of/"+target
        resp = requests.get(url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
        domain_result = re.findall("'([^<>\"/]*?\."+target+")",resp.text)
        for subdomain in domain_result:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
        print("Complete search_subdomain_from_findsubdomain")

    except Exception as e:
        print("search_subdomain_from_findsubdomain  error %s" % e.args)
        print("retrying ....")
        time.sleep(5)
        from_findsubdomain(target)

def from_virustotal(target):
    try:
        print("Start search_subdomain_from_virustotal")
        url = "https://www.virustotal.com/ui/domains/"+target+"/subdomains?limit=30"
        resp = requests.get(url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
        result = json.loads(resp.text)
    except Exception as e:
        print("search_subdomain_from_virustotal connect error"),e.args
    for i in range(len(result["data"])):
        #print(result["data"][i]["id"])
        if result["data"][i]["id"] not in subdomains:
            subdomains.append(result["data"][i]["id"])
    time.sleep(1)
    while "next" in result["links"]:
        try:
            resp = requests.get(result["links"]["next"], timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
            result = json.loads(resp.text)
            for i in range(len(result["data"])):
                #print(result["data"][i]["id"])
                if result["data"][i]["id"] not in subdomains:
                    subdomains.append(result["data"][i]["id"])
            time.sleep(1)

        except:
            continue
    print("Complete search_cert_from_virustotal")

def from_crtsh(target):
    print("Start search_subdomain_from_crtsh")
    try:
        url="https://crt.sh/?q=%25."+target
        page=requests.get(url,timeout=30, headers={"User-Agent": random.choice(USER_AGENTS)})
        soup = BeautifulSoup(page.text, "html.parser")
        td_list = soup.find_all("td")
        # print (td_list)
        for td in td_list:

            if (len(td.text) < 200):
                if "kuaishou.com" in td.text and "LIKE" not in td.text:
                    func=td.text
                    func_domain=func.replace("*.","")
                    if func_domain not in subdomains:
                        subdomains.append(func_domain)
    except Exception as e:
        print(e.args)
        print("restring...")

    print("Complete search_cert_from_crt")


def from_baidu(target,page_num):
    try:
        #print (u'[+] 正在爬取第 %d 页'%(page_num/10+1))
        #print ('第{}页'.format(page_num/10))
        print("start search from baidu")
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:%s'%(target,page_num,target)
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

                if  len(re.findall('/\w',sub_domain)) == 0 and sub_domain not in subdomains:
                    sub_domain = sub_domain.replace('/', '')
                    #print (sub_domain)
                    subdomains.append(sub_domain)
                else:
                    pass

        if r'class="n">下一页' in content:
            new_page_num = page_num + 10
            time.sleep(1)
            from_baidu(target,new_page_num)
    except Exception as e:
        print("search from baidu error! %s" % e.args)
        print("restring...")
        from_baidu(target, 0)



if __name__ == '__main__':
    top_damain="kuaishou.com"
    from_virustotal(top_damain)     #测试通过
    from_findsubdomain(top_damain)  #测试通过
    from_crtsh(top_damain)         #测试通过
    #from_threatcrowd(top_damain)    #没法得到爬取结果，并且结果太少 ,放弃
    from_baidu(top_damain,0)      #测试通过

    with open("output_sudomain.txt", "w+") as f:

        for subdomain in subdomains:
            f.write(subdomain+"\r\n")
    f.close()
    print("all subdomain scan complete！！")
    

