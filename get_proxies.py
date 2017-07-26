import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    }

def parse_ip181(text):
    soup = BeautifulSoup(text, 'html.parser')
    proxies = {}
    for row in soup.select('table tr'):
        col = [ c.text.strip() for c in row.find_all('td') ]
        if re.match(r'\d+\.\d+\.\d+\.\d+', col[0]) and re.match('\d+', col[1]):
            p = '{}:{}'.format(col[0], col[1])
            try:
                r = requests.get('http://www.taobao.com', headers=headers, proxies={ 'http': p }, timeout=3)
                proxies.setdefault(p, 1)
            except:
                # except ProxyError as e:
                print("SKIP:", p, len(proxies))

        #if len(self.proxies) >= n:
        #    break
    return proxies

def parse_freelist(text):
    soup = BeautifulSoup(text, 'html.parser')
    proxies = {}
    for row in soup.select('#proxylisttable tr'):
        col = [ c.text.strip() for c in row.find_all('td') ]
        if len(col) < 2: continue
        if re.match(r'\d+\.\d+\.\d+\.\d+', col[0]) and re.match('\d+', col[1]):
            p = '{}:{}'.format(col[0], col[1])
            try:
                r = requests.get('http://www.google.com', headers=headers, proxies={ 'http': p }, timeout=3)
                proxies.setdefault(p, 1)
            except:
                # except ProxyError as e:
                print("SKIP:", p, len(proxies))

        #if len(self.proxies) >= n:
        #    break
    return proxies


def get_page(url, rid, output, fparse):
    r = requests.get(url, headers=headers)
    with open('{:03d}_{}'.format(rid, output), 'wb') as f:
        f.write(r.content)
    with open('{:03d}_{}'.format(rid, output), 'r', errors='ignore') as f:
        return fparse(f.read())


class ProxyPool:
    def __init__(self, proxyfile = None):
        self.proxies = {}
        self._dead = {}
        self.test_url = 'http://www.apple.com'
        if proxyfile:
            with open(proxyfile, 'r') as f:
                self.proxies.setdefault(f.readline(), 0)

    def search(self):
        self.proxies.update(get_page('http://www.ip181.com', 1, 'proxy_ip181.html', parse_ip181))
        self.proxies.update(get_page('https://free-proxy-list.net/anonymous-proxy.html', 1, 'proxy_freelist.html', parse_freelist))
        with open('proxies.txt', 'w') as f:
            for k,v in self.proxies.items():
                f.write("{}\n".format(k))




p = ProxyPool()
p.search()
