import requests

def criterion_url(url):
    '''
    规范url
    '''
    if 'http' not in url:
        url = 'http://' + url
    if url[-1] != '/':
        url += '/'
    r_url = url + 'robots.txt'
    return (r_url)

def view_robots(url):
    '''
    主函数，启动函数
    '''
    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
    url = criterion_url(url)
    req = requests.get(url,headers=headers)
    if req.status_code == 200:
        return ('[+] Found the robots.txt\n{}'.format(url))
    else:
        return ('[-] Can\'t found the robots.txt\n')
