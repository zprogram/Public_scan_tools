#!/usr/bin/python
#coding:utf-8


# 导入库
import os,sys
import glob     # 遍历子目录文件内容
import logging
import shutil   # 删除目录
from utils.config import *
from utils.from_baidu import from_baidu
from utils.from_bugscaner import *
from utils.from_crtsh import *
from utils.from_findsubdomain import *
from utils.from_netcraft import *
from utils.from_virustotal import *
from utils.from_subDomainsBrute import *   # DNS爆破


# from 目录.文件名 import 函数或类
# from utils.alexa import Alexa

# 日志提示
logging.basicConfig(
    level=logging.INFO, # filename='/tmp/wyproxy.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
)


# 调用库
# 每个功能，写成一个文件，导出txt
def run(domain):
    # init _cache_path
    script_path = os.path.dirname(os.path.abspath(__file__))                # .py文件的绝对路径
    result_path = os.path.join(script_path, 'result/{0}'.format(domain))  #  缓存路径
    if not os.path.exists(result_path):
        os.makedirs(result_path, 0777)                                      #  建立result目录内域名对应的目录
    
    #   from crtsh
    logging.info("starting crtsh fetcher...")
    result_file = os.path.join(result_path, 'crtsh.txt')  # 输出的文件名
    result=from_crtsh(domain)
    result = check_repeated(result)                         # 去重复函数
    save_result(result_file,result)                         # 保存文件结果
    logging.info("crtsh fetcher ({0}) subdomains({1}) successfully...".format(domain,len(result)))

    #   from netcraft
    logging.info("starting netcraft fetcher...")
    result_file = os.path.join(result_path, 'netcraft.txt')  # 输出的文件名
    result=from_netcraft(domain)
    result = check_repeated(result)                         # 去重复函数
    save_result(result_file,result)                         # 保存文件结果
    logging.info("netcraft fetcher ({0}) subdomains({1}) successfully...".format(domain,len(result)))

    #   from virtustotal
    logging.info("starting virtustotal fetcher...")
    result_file = os.path.join(result_path, 'virtustotal.txt')  # 输出的文件名
    result=from_virustotal(domain)
    result = check_repeated(result)                         # 去重复函数
    save_result(result_file,result)                         # 保存文件结果
    logging.info("virtustotal fetcher ({0}) subdomains({1}) successfully...".format(domain,len(result)))


    #   from findsubdomain
    logging.info("starting findsubdomain fetcher...")
    result_file = os.path.join(result_path, 'findsubdomain.txt')  # 输出的文件名
    result = from_findsubdomain(domain)
    result = check_repeated(result)  # 去重复函数
    save_result(result_file, result)  # 保存文件结果
    logging.info("findsubdomain fetcher ({0}) subdomains({1}) successfully...".format(domain, len(result)))


    #   from bugscaner
    logging.info("starting bugscaner fetcher...")
    result_file = os.path.join(result_path, 'bugscaner.txt')  # 输出的文件名
    result = from_bugscaner(domain)
    result = check_repeated(result)  # 去重复函数
    save_result(result_file, result)  # 保存文件结果
    logging.info("bugscaner fetcher ({0}) subdomains({1}) successfully...".format(domain, len(result)))

    #   from baidu
    logging.info("starting baidu fetcher...")
    result_file = os.path.join(result_path, 'baidu.txt')  # 输出的文件名
    result = from_baidu(domain,0)
    result = check_repeated(result)  # 去重复函数
    save_result(result_file, result)  # 保存文件结果
    logging.info("baidu fetcher ({0}) subdomains({1}) successfully...".format(domain, len(result)))
  																		
    #   from subDomainsBrute
    logging.info("starting subDomainsBrute fetcher...")
    result_file = os.path.join(result_path, 'subDomainsBrute.txt')  # 输出的文件名
    result = from_SubDomainBrute(domain)  # 函数实现
    result = check_repeated(result)        # 去重复函数
    save_result(result_file,result)        # 保存文件结果
    logging.info("subDomainsBrute fetcher ({0}) subdomains({1}) successfully...".format(domain,len(result)))

# 去重复函数
def check_repeated(one_list):
    '''
    使用排序的方法
    '''
    result_list = []
    temp_list = sorted(one_list)
    i = 0
    while i < len(temp_list):
        if temp_list[i] not in result_list:
            result_list.append(temp_list[i])
        else:
            i += 1
    return result_list

# 输出结果
def outfile():
    with open(out_domain_result, 'w') as f:           # 输出路径结果 domain_result.txt
        for _file in glob.glob(out_dir + '*.txt'):
            with open(_file, 'r') as tmp_f:
                content = tmp_f.read()
            f.write(content)
    print('[+] The output file is %s' % out_domain_result)

# 读文件
def read_file(domain_path):
    target = []
    # 判断文件路径是否存在，如果不存在直接退出，否则读取文件内容
    if (not os.path.exists(domain_path)):
        print ('Please confirm correct filepath!')
        sys.exit(0)
    else:
        # target
        with open(domain_path, 'r') as source:
            for line in source:
                target.append(line.rstrip('\r\n').rstrip('\n'))
    return target


# 保存单个函数测试的结果
def save_result(filename,result):
    with open(filename, 'w') as fd:
        for result_value in result:
            fd.write(result_value+"\n")

# 主函数
if __name__ == '__main__':
    # 读取文件
    target = read_file(domain_files)
    # 批量运行查询子域名
    for target_list in target:
        run(target_list)    # 单个查询
    # 从批量的结果中读取文本，然后汇总到起来
    outfile()