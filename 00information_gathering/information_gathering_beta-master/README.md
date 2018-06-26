# 5.24 更新

## 暑假重新整理这个仓库，优化结构

# infomation_gathering_beta

#### beta版目前实现了以下功能
```
功能表
  1. CMS识别  cms_map.py    2个类 main()  1个目录扫描  1个调用API   (√)
  2. Whois查询    whois_chinaz.py    1个类 main()  站长之家API (√)
  3. 子域名查询  subdomain_gathering.py  1个类 main()  site:domain 查询 (√)
  4. CDN识别  cdn_finder.py (√)
  5. 常用端口扫描以及对应服务 port_scan.py 1个类 main() 调用 python-nmap库(√)
  6. whatweb扫描  网站脚本语言 IP 搭建平台  whatweb.py 1个类 main() 调用whatweb (√)
  7. 操作系统   whatweb 或者 nmap 可以探测    (√)
  8. Robots 文件探测
```
## Environment:
* python 3.6
* windows or linux
* nmap

## Download:::
```
git clone https://github.com/damit5/information_gathering_beta.git

pip installer -r requirement.txt
```

## Usage:::
```
python main.py url

eg:
python main.py http://www.discuz.net/
```
