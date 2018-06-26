# coding:utf-8

import os,requests,threading,Queue,sys
from optparse import OptionParser

event = threading.Event()
event.set()

def ScanFile(filename,queue):
    filename = filename+'.txt'
    if filename in os.listdir(os.getcwd()+'/Bin/'):
        with open(os.getcwd()+'/Bin/'+filename) as f:
            lines = f.readlines()

        return map(lambda x:queue.put(x.split('\r\n')[0]),lines)

class DirScanner(threading.Thread):

    def __init__(self,url,queue):
        threading.Thread.__init__(self)
        self.url = url
        self.queue = queue

    def run(self):
        self.header={"User-Agent":"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"}
        while event.isSet():
            if self.queue.empty():
            	event.clear()
                exit(0)
            else:
                try:
                    url = self.url+self.queue.get_nowait()
                
                    req = requests.get(url,timeout=10, allow_redirects=False, headers = self.header)

                except Queue.Empty:
                	event.clear()
                	exit(0)
                except KeyboardInterrupt,e:
                    continue
                except Exception,e:
                    continue
                if req.status_code == 200:
                    print '<200> '+url
                elif req.status_code == 403:
                    print '<403> '+url
                elif req.status_code == 302:
                    print '<302> '+url
                else:
                    continue

def main(url,ScriptName,thread_num=10):
    q = Queue.Queue(-1)
    ScanFile('DIR',q)
    ScanFile('MDB',q)
    if ScriptName.upper() in ['ASP','JSP','PHP','ASPX']:
        ScanFile(ScriptName.upper(),q)
    else:
        print u'请输入正确的脚本名'
        exit(0)

    threads = []
    for num in xrange(int(thread_num)):
        threads.append(DirScanner(url,q))
    for t in threads:
        t.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    usage = '[-u <Website/Target_url>][-t <Scan thread num>]'
    parser = OptionParser(usage)
    parser.add_option('-u',dest='target_url',help='Example:-u http://www.example.com')
    parser.add_option('-s',dest='webScript',help='Example:-s asp')
    parser.add_option('-t',dest='thread_num',type='int',default=10,help='Example:-t 50')
    options,args=parser.parse_args()

    if options.target_url[:4] == 'http' and options.webScript:
    	main(options.target_url,options.webScript,options.thread_num)
    else:
        print usage
