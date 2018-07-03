# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
import requests
import re

def from_chaxun_la(domain):
    subdomains = []
    try:
        for page in xrange(10):
            url = "http://api.chaxun.la/toolsAPI/getDomain/?k={}&page={}&order=default&sort=desc&action=moreson".format(
                domain, page)
            r = requests.get(url)
            context = r.text.encode('utf-8').decode('utf-8-sig')
            context = context.split(",")
            for value in context:
                matchObj = re.match(r'"domain":"(.*)"', value, re.M | re.I)
                if matchObj:
                    subdomains.append(matchObj.group(1))
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))




