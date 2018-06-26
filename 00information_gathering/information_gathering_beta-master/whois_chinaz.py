import requests
import re
from bs4 import BeautifulSoup

class whois:
    '''
    method = 1 邮箱反查
    method = 2 注册人反查
    method = 3 电话反查
    method = None 查询所有
    '''
    def __init__(self,url,method=None):
        self.url = url.strip('/').replace('http://','').replace('https://','')
        self.method = method
        self.headers = {'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv'}

    def whois(self):
        '''    # whois查询。返回查询结果（需要 反向查询的信息 以及 whois信息）'''
        url = 'http://whois.chinaz.com/%s'%self.url
        self.headers['Referer'] = 'http://whois.chinaz.com/'
        cookies = {'qHistory': 'aHR0cDovL2lwLmNoaW5hei5jb20rSVAv5pyN5Yqh5Zmo5Zyw5Z2A5p+l6K+ifGh0dHA6Ly9pY3AuY2hpbmF6LmNvbS8r572R56uZ5aSH5qGIfGh0dHA6Ly93aG9pcy5jaGluYXouY29tL3JldmVyc2UrV2hvaXPlj43mn6V8aHR0cDovL3dob2lzLmNoaW5hei5jb20vK1dob2lz5p+l6K+ifGh0dHA6Ly90b29sLmNoaW5hei5jb20r56uZ6ZW/5bel5YW3'}
        data = {'ws': 'whois.webnic.cc', 'DomainName': self.url}
        content = requests.post(url,headers=self.headers,cookies=cookies,data=data).content
        soup = BeautifulSoup(content,'lxml')
        soup = soup.find('div',class_="WhoisWrap clearfix")  # 缩小匹配范围
        try:
            registrar = soup.find('div',class_='block ball').get_text() # 注册商
        except:
            registrar = ''
        try:
            re_contactor = '联系人</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>'
            contactor = re.findall(re_contactor,str(soup))[0]   # 联系人
        except:
            contactor = ''
        try:
            re_email = '联系邮箱</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>'
            email = re.findall(re_email,str(soup))[0]   # 联系邮箱
        except:
            email = ''
        try:
            re_phone = '联系电话</div><div class="fr WhLeList-right block ball lh24"><span>(.*?)</span>'
            phone = re.findall(re_phone,str(soup))[0]   # 联系电话
        except:
            phone = ''
        try:
            re_creat_time = '创建时间</div><div class="fr WhLeList-right"><span>(.*?)</span>'
            creat_time = re.findall(re_creat_time,str(soup))[0] # 创建时间
        except:
            creat_time = ''
        try:
            re_overdue_time = '过期时间</div><div class="fr WhLeList-right"><span>(.*?)</span>'
            overdue_time = re.findall(re_overdue_time,str(soup))[0] # 过期时间
        except:
            overdue_time = ''
        try:
            re_domain_server = '域名服务器</div><div class="fr WhLeList-right"><span>(.*?)</span>'
            domain_server = re.findall(re_domain_server,str(soup))[0]   # 域名服务器
        except:
            domain_server = ''
        try:
            re_dns = 'DNS</div><div class="fr WhLeList-right">(.*?)</div>'
            dns = re.findall(re_dns,str(soup))[0].replace('<br/>','\n').replace(' ','')    # DNS
        except:
            dns = ''

        # 返回所有查询到的内容，用 \n 作为分隔符
        return_content = '注册商:' + registrar + '\n' + '联系人:' + contactor + '\n' + '联系邮箱:' + email + '\n' + '联系电话:' + phone + '\n' + '创建时间:' + creat_time + '\n' + '过期时间:' + overdue_time + '\n' + '域名服务器:' + domain_server + '\n' + 'DNS:' + dns

        if self.method == 1:
            return email,return_content
        elif self.method == 2:
            return contactor,return_content
        elif self.method == 3:
            return phone,return_content
        else:
            return '|'.join([email,contactor,phone]),return_content

    def reverse_whois(self,keyword,method):
        '''# 反向查询 method 为查询方法，keyword为关键词'''
        url = 'http://whois.chinaz.com/reverse?host=%s&ddlSearchMode=%s'%(str(keyword).replace(' ','+'),str(method))
        self.headers['Referer'] = url
        cookies = {'qHistory': 'aHR0cDovL2lwLmNoaW5hei5jb20rSVAv5pyN5Yqh5Zmo5Zyw5Z2A5p+l6K+ifGh0dHA6Ly9pY3AuY2hpbmF6LmNvbS8r572R56uZ5aSH5qGIfGh0dHA6Ly93aG9pcy5jaGluYXouY29tL3JldmVyc2UrV2hvaXPlj43mn6V8aHR0cDovL3dob2lzLmNoaW5hei5jb20vK1dob2lz5p+l6K+ifGh0dHA6Ly90b29sLmNoaW5hei5jb20r56uZ6ZW/5bel5YW3'}
        data = {'host': '%s'%str(keyword).replace(' ',''), 'ddlSearchMode': str(method)}
        content = requests.post(url,headers=self.headers,cookies=cookies,data=data).content
        soup = BeautifulSoup(content,'lxml')
        # 找到所有的信息
        all_info_one = soup.findAll('li',class_='WhoListCent Wholist clearfix bor-b1s02')
        all_info_two = soup.findAll('li',class_='WhoListCent Wholist clearfix bor-b1s02 bg-list')
        all_info = all_info_one + all_info_two
        for info in all_info:
            #每一行信息，包括域名、邮箱、电话、注册商、DNS、注册时间、过期时间
            save_info = [] # 用 list 来保存一条记录的所有信息
            one_info = info.strings
            num = one_info.__next__()   # 序号
            #save_info.append(num)
            domain = one_info.__next__()    #域名
            save_info.append(domain)
            email = one_info.__next__() # 注册人|邮箱|注册人
            save_info.append(email)
            phone = one_info.__next__() # 电话
            save_info.append(phone)
            registrar = one_info.__next__() # 注册商
            save_info.append(registrar)
            dns = one_info.__next__()   # dns
            while True:
                # dns不止一个的时候，通过判断第一位来查看后面的是否也为dns
                tmp = one_info.__next__()
                if str(tmp)[0] not in ['1','2','3','4','5','6','7','8','9','0']:
                    dns = dns + ';' + tmp
                else:
                    save_info.append(dns)
                    registration_time = tmp # 注册时间
                    save_info.append(registration_time)
                    break
            overdue_time = one_info.__next__()   # 到期时间
            save_info.append(overdue_time)
            yield save_info

    def main(self):
        # 定义 results 变量，作为 return 的值传送出去
        results = []
        result = self.whois()
        results.append(result[1]) # 输出 whois 的查询结果

        '''
        if self.method == 1:
            print '\n邮箱反查结果：\n'
        elif self.method == 2:
            print '\n注册人反查结果：\n'
        elif self.method == 3:
            print '\n电话反查结果：\n
        else:
            print ('\nALL INFO\n')
        '''

        keyword = result[0]
        # 反查的结果
        if self.method == None:
            '''
            如果没有指定参数，就把所有的信息全部查询出来
            '''
            email,contactor,phone = keyword.split('|')
            results.append('\ne-mail 反查结果：\n')
            generator = self.reverse_whois(email,1)
            for info in generator:
                results.append(info[0] + '  ' + info[1] + '  ' + info[2] + '  ' + info[3] + '  ' + info[4] + '  ' + info[5] + '  ' + info[6] + '\n')
            results.append('\n注册人 反查结果：\n')
            generator = self.reverse_whois(contactor,2)
            for info in generator:
                results.append(info[0] + '  ' + info[1] + '  ' + info[2] + '  ' + info[3] + '  ' + info[4] + '  ' + info[5] + '  ' + info[6] + '\n')
            results.append('\n手机 反查结果：\n')
            generator = self.reverse_whois(phone,3)
            for info in generator:
                results.append(info[0] + '  ' + info[1] + '  ' + info[2] + '  ' + info[3] + '  ' + info[4] + '  ' + info[5] + '  ' + info[6] + '\n')
        else:
            '''
            指定了 method 的参数
            '''
            generator = self.reverse_whois(keyword,self.method)
            for info in generator:
                results.append(info[0] + '  ' + info[1] + '  ' + info[2] + '  ' + info[3] + '  ' + info[4] + '  ' + info[5] + '  ' + info[6] + '\n')

        return results
