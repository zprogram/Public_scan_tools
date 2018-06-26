# -*- coding:utf-8 -*-
import nmap
import socket
import re

class port_scan:
    def __init__(self,url):
        try:
            self.host = socket.gethostbyname(url.replace('http://','').replace('https://','').replace('/',''))
        except:
            self.host = None

    def nmap_scan(self):
        if self.host == None:
            return 'Error! Are you sure your domain is right ?'
        nm= nmap.PortScanner()
        nm.scan(hosts='%s'%self.host, ports=None, arguments='-Pn -F -n -T4 -sV -O', sudo=False)
        state = nm[self.host].state()   # 主机状态
        result = [] # 定义 return 的内容
        result.append('Host : %s '%(self.host))
        result.append('State : %s'%nm[self.host].state())
        result.append('---------------------------')
        #print ('---------------------------')
        #all_protocols = nm[self.host].all_protocols()
        for port in nm[self.host].all_tcp(): # 获取tcp协议所有的端口号 (按照端口号大小进行排序)
            info = nm[self.host]['tcp'][port]
            if info['state'] == 'open':
                result.append('port:\t%d'%port)
                #print 'state:\t' + info['state']
                result.append('version:' + info['version'])
                result.append('name:\t' + info['name'])
                result.append('cpe:\t' + info['cpe'] + '\n')
                #print '\n'
        return result

    def main(self):
        result = self.nmap_scan()
        return result
