#!/usr/bin/python
#coding:utf-8


import multiprocessing
import gevent
from gevent import monkey
monkey.patch_all()
from gevent.queue import PriorityQueue
import re
import dns.resolver
import time
import signal
import glob
import optparse
from gevent.pool import Pool
import shutil
from config import *   #调用参数
import logging

# 日志提示
logging.basicConfig(
    level=logging.INFO, # filename='/tmp/wyproxy.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
)
start_time = time.time()

class SubNameBrute:
    def __init__(self, target, process_num, dns_servers, next_subs,
                 scan_count, found_count, queue_size_list, tmp_dir):
        self.target = target.strip()
        self.process_num = process_num
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)
        self.next_subs = next_subs
        self.scan_count = scan_count
        self.scan_count_local = 0
        self.found_count = found_count
        self.found_count_local = 0
        self.queue_size_list = queue_size_list

        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(threads_count)]
        for _r in self.resolvers:
            _r.lifetime = _r.timeout = 6.0
        self.queue = PriorityQueue()
        self.item_index = 0
        self.priority = 0
        self._load_sub_names()
        self.ip_dict = {}
        self.found_subs = set()
        self.ex_resolver = dns.resolver.Resolver(configure=False)
        self.ex_resolver.nameservers = dns_servers
        self.local_time = time.time()
        self.outfile = open('%s/%s_part_%s.txt' % (tmp_dir, target, process_num), 'w') #  建立目录

    def _load_sub_names(self):
        if doamin_dict=="full":
            current_path = os.path.dirname(__file__)  # 返回当前文件所在的目录
            dict_path = os.path.dirname(current_path)  # 获得d所在的目录,即d的父级目录
            _file = dict_path+'/dict/next_sub_full.txt'
        else:
            if os.path.exists(doamin_dict):
                _file = doamin_dict
            else:
                logging.info("[ERROR] Names file not found: {0}".format(doamin_dict))
                exit(-1)
			
        normal_lines = []
        wildcard_lines = []
        wildcard_list = []
        regex_list = []
        lines = set()
        with open(_file) as f:
            for line in f.xreadlines():
                sub = line.strip()
                if not sub or sub in lines:
                    continue
                lines.add(sub)

                if sub.find('{alphnum}') >= 0 or sub.find('{alpha}') >= 0 or sub.find('{num}') >= 0:
                    wildcard_lines.append(sub)
                    sub = sub.replace('{alphnum}', '[a-z0-9]')
                    sub = sub.replace('{alpha}', '[a-z]')
                    sub = sub.replace('{num}', '[0-9]')
                    if sub not in wildcard_list:
                        wildcard_list.append(sub)
                        regex_list.append('^' + sub + '$')
                else:
                    normal_lines.append(sub)
        if regex_list:
            pattern = '|'.join(regex_list)
            _regex = re.compile(pattern)
            for line in normal_lines[:]:
                if _regex.search(line):
                    normal_lines.remove(line)

        for item in normal_lines[self.process_num::process_count]:
            self.priority += 1
            self.queue.put((self.priority, item))

        for item in wildcard_lines[self.process_num::process_count]:
            self.queue.put((88888888, item))

    def put_item(self, item):
        num = item.count('{alphnum}') + item.count('{alpha}') + item.count('{num}')
        if num == 0:
            self.priority += 1
            self.queue.put((self.priority, item))
        else:
            self.queue.put((self.priority + num * 10000000, item))

    def _scan(self, j):
        self.resolvers[j].nameservers = [self.dns_servers[j % self.dns_count]]
        while not self.queue.empty():
            try:
                item = self.queue.get(timeout=3.0)[1]
                self.scan_count_local += 1
                if time.time() - self.local_time > 3.0:
                    self.scan_count.value += self.scan_count_local
                    self.scan_count_local = 0
                    self.queue_size_list[self.process_num] = self.queue.qsize()
            except Exception as e:
                break
            try:
                if item.find('{alphnum}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                        self.put_item(item.replace('{alphnum}', _letter, 1))
                    continue
                elif item.find('{alpha}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz':
                        self.put_item(item.replace('{alpha}', _letter, 1))
                    continue
                elif item.find('{num}') >= 0:
                    for _letter in '0123456789':
                        self.put_item(item.replace('{num}', _letter, 1))
                    continue
                elif item.find('{next_sub}') >= 0:
                    for _ in self.next_subs:
                        self.queue.put((0, item.replace('{next_sub}', _, 1)))
                    continue
                else:
                    sub = item

                if sub in self.found_subs:
                    continue

                cur_sub_domain = sub + '.' + self.target
                _sub = sub.split('.')[-1]
                try:
                    answers = self.resolvers[j].query(cur_sub_domain)
                except dns.resolver.NoAnswer, e:
                    answers = self.ex_resolver.query(cur_sub_domain)

                if answers:
                    self.found_subs.add(sub)
                    ips = ', '.join(sorted([answer.address for answer in answers]))
                    if ips in ['1.1.1.1', '127.0.0.1', '0.0.0.0']:
                        continue

                    if domain_ips and is_intranet(answers[0].address):
                        continue

                    try:
                        self.scan_count_local += 1
                        answers = self.resolvers[j].query(cur_sub_domain, 'cname')
                        cname = answers[0].target.to_unicode().rstrip('.')
                        if cname.endswith(self.target) and cname not in self.found_subs:
                            self.found_subs.add(cname)
                            cname_sub = cname[:len(cname) - len(self.target) - 1]    # new sub
                            self.queue.put((0, cname_sub))

                    except:
                        pass

                    if (_sub, ips) not in self.ip_dict:
                        self.ip_dict[(_sub, ips)] = 1
                    else:
                        self.ip_dict[(_sub, ips)] += 1
                        if self.ip_dict[(_sub, ips)] > 30:
                            continue

                    self.found_count_local += 1
                    if time.time() - self.local_time > 3.0:
                        self.found_count.value += self.found_count_local
                        self.found_count_local = 0
                        self.queue_size_list[self.process_num] = self.queue.qsize()
                        self.local_time = time.time()

                    logging.info("{0}".format(cur_sub_domain.ljust(30) + ips))
                    self.outfile.write(cur_sub_domain.ljust(30) + '\t' + ips + '\n')
                    self.outfile.flush()
                    try:
                        self.resolvers[j].query('lijiejietest.' + cur_sub_domain)   # ？？
                    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
                        self.queue.put((999999999, '{next_sub}.' + sub))
                    except:
                        pass

            except (dns.resolver.NXDOMAIN, dns.name.EmptyLabel) as e:
                pass
            except (dns.resolver.NoNameservers, dns.resolver.NoAnswer, dns.exception.Timeout) as e:
                pass
            except Exception as e:
                import traceback
                traceback.print_exc()
                with open('errors.log', 'a') as errFile:
                    errFile.write('[%s] %s %s\n' % (type(e), cur_sub_domain, str(e)))

    def run(self):
        threads = [gevent.spawn(self._scan, i) for i in range(threads_count)]
        gevent.joinall(threads)





def run_process(target, process_num, dns_servers, next_subs, scan_count, found_count, queue_size_list,
                tmp_dir):
    signal.signal(signal.SIGINT, user_abort)
    s = SubNameBrute(target=target, process_num=process_num,
                     dns_servers=dns_servers, next_subs=next_subs,
                     scan_count=scan_count, found_count=found_count, queue_size_list=queue_size_list,
                     tmp_dir=tmp_dir)
    s.run()


def is_intranet(ip):
    ret = ip.split('.')
    if len(ret) != 4:
        return True
    if ret[0] == '10':
        return True
    if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
        return True
    if ret[0] == '192' and ret[1] == '168':
        return True
    return False


# 信号
def user_abort(sig, frame):
    exit(-1)

# 载入二级域名
def load_next_sub():
    next_subs = []
    _set = set()                               # 字典值
    current_path = os.path.dirname(__file__)  # 返回当前文件所在的目录
    dict_path = os.path.dirname(current_path)  # 获得d所在的目录,即d的父级目录
    dict_file = dict_path+'/dict/next_sub_full.txt' if doamin_dict=="full" else  dict_path+'/dict/next_sub.txt'   # 字典路径，如果选择全部扫描（full）就采用next_sub_full.txt字典，否则就用dict/next_sub.txt
    with open(dict_file) as f:
        for line in f:
            sub = line.strip()
            if sub and sub not in next_subs:
                tmp_set = {sub}
                while tmp_set:
                    item = tmp_set.pop()
                    if item.find('{alphnum}') >= 0:                                     # 可定制变量(a-z,0-9)
                        for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            tmp_set.add(item.replace('{alphnum}', _letter, 1))
                    elif item.find('{alpha}') >= 0:
                        for _letter in 'abcdefghijklmnopqrstuvwxyz':                 # 可定制变量(a-z)
                            tmp_set.add(item.replace('{alpha}', _letter, 1))
                    elif item.find('{num}') >= 0:                                        # 可定制变量(0-9)
                        for _letter in '0123456789':
                            tmp_set.add(item.replace('{num}', _letter, 1))
                    elif item not in _set:
                        _set.add(item)
                        next_subs.append(item)
    return next_subs



# 测试DNS准确性
# 测试存在的域名和不存在的域名，如果DNS解析正确，加入查询服务器列表。否则记录为错误的DNS服务器，保存为文件
def test_server(server, dns_servers):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.lifetime = resolver.timeout = 6.0
    try:
        resolver.nameservers = [server]
        answers = resolver.query('public-dns-a.baidu.com')    # test lookup an existed domain
        if answers[0].address != '180.76.76.76':
            raise Exception('Incorrect DNS response')
        try:
            resolver.query('test.bad.dns.17bdw.com')    # Non-existed domain test
            with open('bad_dns_servers.txt', 'a') as f:
                f.write(server + '\n')
            logging.info("[+] Bad DNS Server found {0}".format(server))
        except:
            dns_servers.append(server)
        logging.info("[+] Server {0} < OK >   Found {1}".format(server.ljust(16), len(dns_servers)))
    except:
        logging.info("[+] Server {0} <Fail>   Found {1}".format(server.ljust(16), len(dns_servers)))

# 载入DNS服务器测试
def load_dns_servers():
    dns_servers = []
    pool = Pool(10)

    current_path = os.path.dirname(__file__)  # 返回当前文件所在的目录
    dict_path = os.path.dirname(current_path)  # 获得d所在的目录,即d的父级目录
    for server in open(dict_path+'/dict/dns_servers.txt').readlines():
        server = server.strip()
        if server:
            pool.apply_async(test_server, (server, dns_servers))
    pool.join()

    dns_count = len(dns_servers)
    logging.info("[+] {0} available DNS Servers found in total".format(dns_count))
    if dns_count == 0:
        logging.info("[ERROR] No DNS Servers available!".format(dns_count))
        sys.exit(-1)
    return dns_servers

# 主要实现函数
def from_SubDomainBrute(target):
   # {'full_scan': True, 'process': 6, 'i': False, 'threads': 200, 'file': 'subnames.txt', 'output': None}
    # 删除文件
    tem_dir = os.getcwd() + "\\tmp\\"
    if os.path.exists(tem_dir):
        shutil.rmtree(tem_dir)

    tmp_dir = os.getcwd()+'//tmp/%s_%s' % (target, int(time.time()))
    if not os.path.exists(tmp_dir):  # 生成路径
        os.makedirs(tmp_dir)

    multiprocessing.freeze_support()
    all_process = []
    dns_servers = load_dns_servers()     # 载入DNS服务器
    next_subs = load_next_sub()          # 载入二级域名字典
    scan_count = multiprocessing.Value('i', 0)
    found_count = multiprocessing.Value('i', 0)
    queue_size_list = multiprocessing.Array('i', process_count)   # 指定线程数

    try:
        print '[+] Init %s scan process.' % process_count
        for process_num in range(process_count):
            p = multiprocessing.Process(target=run_process,
                                        args=(target, process_num,
                                              dns_servers, next_subs,
                                              scan_count, found_count,queue_size_list,
                                              tmp_dir)
                                        )
            all_process.append(p)
            p.start()

        while all_process:
            for p in all_process:
                if not p.is_alive():
                    all_process.remove(p)    # 如果进程结束就退出
            groups_count = 0
            for c in queue_size_list:
                groups_count += c
            # logging.info("[*] {0} found, {1} scanned in {2:.1f} seconds,{3} groups left".format(found_count.value, scan_count.value, time.time() - start_time, groups_count))
            time.sleep(1.0)
    except KeyboardInterrupt as e:
        for p in all_process:
            p.terminate()
        print '[ERROR] User aborted the scan!'
    except Exception as e:
        print e

    logging.info("[+] All Done. {0} found, {1} scanned in {2:.1f} seconds.".format(found_count.value, scan_count.value, time.time() - start_time))
    result = []
    # 输出路径位置，这里改成返回列表
    for _file in glob.glob(tmp_dir + '/*.txt'):
        with open(_file, 'r') as tmp_f:
            for line in tmp_f:
                result.append(line.split()[0])
    # 删除文件
    shutil.rmtree(tem_dir)
    return  result