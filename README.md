## To Do List

- 20170626~0629 1-信息收集-子域名方法集合


| 测试人员 | 测试目标                          | 测试结果 |  备注                                                                                                      |
| -------- | --------------------------------- | -------- | --------                                                                                                   |
| skeep    | information_gathering_beta-master |  测试无误，可以正常运行 |  主要是利用百度搜索引擎来查询子域名 ,https://www.baidu.com/s?wd=site:%s&pn=%d&oq=site:
| skeep    | InformationCollector-master       | 一共四个函数，正常运行1个，其他三个没法因为使用的是https所以得到的有效结果.明天使用web2.0爬虫重新改写   |    用到的四个查询子域名的站点：[[https://www.virustotal.com/ui/domains/baidu.com/subdomains?limit=30]] [[https://crt.sh/]] [[https://www.threatcrowd.org/graphHtml.php?domain=baidu.com]] [[https://findsubdomains.com/subdomains-of/baidu.com]]                                         |
| lipss    | subDomainsBrute-master            | 字典破解 | 使用DNSPOD 阿里云的公共DNS进行查询，使用字典暴力破解域名，字典路径：dict/next_sub_full.txt、dict/next_sub.txt |
| lipss    | wydomain-wydomain2                |          |                                                                                                            |


- 待定 2-信息收集-Web站点信息收集

- 待定 3-收集测试-Web站点爬取URL

-




