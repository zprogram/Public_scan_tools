import requests
import json
import random
from config import *
import time



def from_virustotal(target):
    subdomains=[]
    try:

        url = "https://www.virustotal.com/ui/domains/"+target+"/subdomains?limit=30"
        resp = requests.get(url, timeout=timeout)
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
            resp = requests.get(result["links"]["next"], timeout=timeout, headers=headers)
            result = json.loads(resp.text)
            for i in range(len(result["data"])):
                #print(result["data"][i]["id"])
                if result["data"][i]["id"] not in subdomains:
                    subdomains.append(result["data"][i]["id"])
            time.sleep(1)

        except:
            continue
    return subdomains
