## To Do List

### 1、信息收集

#### 1.1、子域名收集

- 20170626~0629 1-信息收集-子域名方法集合


| 测试人员 | 测试目标                          | 测试结果 |  备注|
| -------- | --------------------------------- | -------- | --------|
| skeep    | information_gathering_beta-master |  改写完成 |  主要是利用百度搜索引擎来查询子域名 ,https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:
| skeep    | InformationCollector-master       | 改写完成，只有一个threatcrowd ，反扒措施太变态，结果还少放弃使用  |    用到的四个查询子域名的站点：  [[https://www.virustotal.com/ui/domains/baidu.com/subdomains?limit=30]][[https://crt.sh/]]  [[https://www.threatcrowd.org/graphHtml.php?domain=baidu.com]]/(丢弃/)  [[https://findsubdomains.com/subdomains-of/baidu.com]]                                         |
|skeep     |汇总形成 skeep_srider_subdamin_bu_web.py       |一共完成4个函数    from_virustotal   from_baidu   from_crtsh   from_findsubdomain |四个函数得到的子域名结果写入到output_subdomain.txt中|
|skeep| 在新的框架中完成6个功能函数|函数结果正常|晚上lipss发来新的可以查询的网站，后续处理|
| lipss    | subDomainsBrute-master            | 字典破解 | 使用DNSPOD:182.254.116.116\119.29.29.29
|          |                                   |          | 阿里云的公共DNS:223.5.5.5\223.6.6.6
|          |                                   |          | 进行查询，使用字典暴力破解域名，字典路径：dict/next_sub_full.txt、dict/next_sub.txt |
| lipss    | wydomain-wydomain2                |          |                                                                                                            |

- 20180701 合并方法
    - 讨论完成子域名搜集的大体框架
    - skeep 完成从6个网站搜集子域名的功能函数,具体用到的网站如下
        - baidu.com
        - bugscaner
        - crt.sh
        - findsubdomain
        - netcraft
        - virustotal
- 20180703 完善方法
    - 修复重复结果的Bug
	- zprogram补充搜集子域名的功能函数，具体用到的网站如下：
        - chaxun.la
        - subDomainsBrute
        - outfile_去重复
        - 读取domain空值判断
		- 修复virustotal，得不到结果报错问题
		- 测试多个域名探测的阈值为2小时18个域名
		- 修复兼容Linux、Windows问题

#### 1.2、Web站点信息收集
- 20180706~无限期 端口扫描与指纹识别




| 收集项 | 已有框架                          | 测试结果 |  备注                                                                                                      |
| -------- | --------------------------------- | -------- | --------   |
| portmap |Biu-framework                       |  |zzzhhh|
|  |wyportmap                           |  |skeep|
| 指纹识别 |SRCHunter | ||



### 2、漏洞测试

- PocSuite-https://github.com/knownsec/Pocsuite
- Bugscan-POC-https://github.com/xibijj/Bugscan
- w9scan-https://github.com/boy-hack/w9scan
- w8scan-https://github.com/957204459/w8scan

### 3、Web站点爬取URL

- 爬取A标签

