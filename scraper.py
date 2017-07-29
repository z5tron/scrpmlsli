#!/usr/bin/python3

import os
import re
import sys
import json
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import random
import operator

import requests

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def next_proxy(proxies, maxv = 4):
    sorted_x = sorted(proxies.items(), key=operator.itemgetter(1))
    for x in sorted_x:
        if x[1] >= 0: return x[0]
    return None


def check_proxy(proxies):
    try:
        r = requests.get('http://www.google.com', proxies=proxies)
    except:
        return 'Dead'
    r = requests.get('http://icanhazip.com', proxies=proxies)
    print('Good', proxies, r.text, proxies['http'])
    if r.text == proxies['http']:
        return 'High'
    return 'Transparent'


def query_server(conf, proxies):
    
    cookies = {
        #'BrokerOffice_Session': 'SessionCookie=a67816d9-be96-4e7f-97e6-171bcb83980d',
        ##'_ga': 'GA1.2.236589968.1498249286',
        ##'D_SID': '216.223.243.119:zIIXN1U5gPZ1JwZeyUN57bFUUhZceZZE+QypSPR+A3E',
        ##'__utma': '119517141.236589968.1498249286.1500915150.1500917126.4',
        ##'__utmz': '119517141.1498249287.1.1.utmcsr=reachlocal|utmccn=search|utmcmd=cpc|utmctr=(not%20provided)',
        ##'ASP.NET_SessionId': 'nk1la3jahzxvwtz3a25lx4lk',
        ##'ExternalReferrer': '',
        ##'rBW-ListingSearch': '21a8d3df-61d2-4115-91da-10a9d216abe2',
        #'BrokerOffice_Visit': '0=c456d055-8967-4b09-910a-f26951a60d28&1=1224-0-0-False',
        ##'_gid': 'GA1.2.70223099.1500911588',
        ##'MLSLI_tc': '1',
        ##'MLSLI_MobilePopup': '1',
        ##'__utmc': '119517141',
        ##'D_IID': '71FC3A37-EA91-3C28-A5EF-56E4DD48DB63',
        ##'D_UID': 'DD4B35DB-2B93-33CF-9D6D-5968DA1BE8C5',
        ##'D_ZID': '11613518-1A4C-35B5-8007-6851AAE0565E',
        ##'D_ZUID': '2D72399B-3CF4-353F-8FAF-D7A875188928',
        ##'D_HID': '266E733E-0819-3C1D-8FCD-5A2885828201',
        #'rBW-CompareListings': '3aa874e4-2930-4b6b-bf61-338b85cb09a5',
        #'PrevSearchSection': 'ListingSearch',
        ##'.publicauth': '',
        ##'Sml-Login-Action': 'http%253A%252F%252Fwww.mlsli.com%252FListing%252FListingSearch.aspx%25253F%252526search%253D21a8d3df-61d2-4115-91da-10a9d216abe2%252526nextaction%253DSaveSearch',
        ##'Sml-Original-Host': 'http%3A%2F%2Fwww.mlsli.com',
        ##'Sml-Original-Path': '%2FListing%2FListingSearch.aspx',
        ##'rBW-IpLocation': '%257b%2522IPAddressFrom%2522%253a%2522216.223.240.0%2522%252c%2522IPAddressTo%2522%253a%2522216.223.255.255%2522%252c%2522CountryCode%2522%253a%2522US%2522%252c%2522State%2522%253a%2522New%2BYork%2522%252c%2522City%2522%253a%2522Setauket-East%2BSetauket%2522%252c%2522Latitude%2522%253a40.9315%252c%2522Longitude%2522%253a-73.111%252c%2522Timezone%2522%253a%2522America%252fNew_York%2522%252c%2522Pin%2522%253a%257b%2522Lat%2522%253a40.93149948%252c%2522Lon%2522%253a-73.11100006%257d%257d',
        ##'dmp-key': '%2Fdc2%2F_T99%2F7912b096-33d9-4cb4-9c6c-ca230a290a93_M-101164_333359',
        ##'__utmb': '119517141.8.10.1500917126',
        ##'__utmt': '1',
        ##'_gat_adWrapperTracker': '1',
    }

    headers = {
        'Host': 'www.mlsli.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://www.mlsli.com/Listing/ListingSearch.aspx',
        'X-Distil-Ajax': 'ewbqyxfuuweabtdbsd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Form': '{"Criteria/FilterByAddress":["1"],"AutoAdjustMap":["on"],"Criteria/ListingTypeID":["1"],"Criteria/PropertyTypeID":["0x000000000000000000000002","0x000000000000000000000004,0x000000000000001000000000","0x000000000000000080000000","0x040000000000000000000000","0x000000000000000000000020"],"Criteria/Status":["1,5", "2"],"Criteria/LocationJson":["[[{\\"name\\":\\"Three Village Central School District, NY (School District)\\",\\"type\\":\\"School District\\",\\"value\\":\\"Three Village Central School District, NY (School District)\\",\\"isNot\\":false}]]"],"Criteria/SearchMapNELat":41.251184315646896,"Criteria/SearchMapNELong":-72.3761100769043,"Criteria/SearchMapSWLat":40.3195457609537,"Criteria/SearchMapSWLong":-74.0789909362793,"Criteria/Zoom":9,"Criteria/SearchMapStyle":"r","IgnoreMap":true,"ListingSortID":6,"view":"list","first":0,"Criteria/SearchType":"map","SearchTab":"mapsearch-criteria-basicsearch","CLSID":-1,"ResultsPerPage":10}',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    ts = datetime.now().strftime('%s') + '234'


    params = (
        #('searchoverride', '21a8d3df-61d2-4115-91da-10a9d216abe2'),
        ('ts', ts),
        ('', ''),
    )

    data = [
        ('Criteria/FilterByAddress', '1'),
        ('AutoAdjustMap', 'on'),
        ('Criteria/MaxPrice', conf['MaxPrice']),
        ('Criteria/ListingTypeID', '1'),
        ('Criteria/PropertyTypeID', '0x000000000000000000000002'),
        #('Criteria/PropertyTypeID', '0x000000000000000000000004,0x000000000000001000000000'), # condo/Homeowner Assoc
        #('Criteria/PropertyTypeID', '0x000000000000000080000000'), # Multi-Family
        #('Criteria/PropertyTypeID', '0x040000000000000000000000'), # Co-Op
        #('Criteria/PropertyTypeID', '0x000000000000000000000020'), # Timeshare
        ('Criteria/Status', '1,5'), # Active
        ('Criteria/Status', '2'), # Sold
        ('Criteria/LocationJson', '[[{"name":"Three Village Central School District, NY (School District)","type":"School District","value":"Three Village Central School District, NY (School District)","isNot":false}]]'),
        ('Criteria/SearchMapNELat', '41.251184315646896'),
        ('Criteria/SearchMapNELong', '-72.3761100769043'),
        ('Criteria/SearchMapSWLat', '40.3195457609537'),
        ('Criteria/SearchMapSWLong', '-74.0789909362793'),
        ('Criteria/Zoom', '9'),
        ('Criteria/SearchMapStyle', 'r'),
        ('IgnoreMap', 'true'),
        ('ListingSortID', '6'),
        ('view', 'list'),
         ('first', conf['itemFirst']),
        ('Criteria/SearchType', 'map'),
        ('SearchTab', 'mapsearch-criteria-basicsearch'),
        ('CLSID', '-1'),
        ('ResultsPerPage', conf['ResultsPerPage']), # default was 10
    ]
    print(proxies)
    try:
        r = requests.post('http://www.mlsli.com/Include/AJAX/MapSearch/GetListingPins.aspx', headers=headers, params=params, cookies=cookies, data=data, proxies=proxies, timeout=8)
        return r
    except:
        return None

def get_item(url, proxies):
    cookies = {
        #'BrokerOffice_Session': 'SessionCookie=a67816d9-be96-4e7f-97e6-171bcb83980d',
        #'_ga': 'GA1.2.236589968.1498249286',
        #'D_SID': '216.223.243.119:zIIXN1U5gPZ1JwZeyUN57bFUUhZceZZE+QypSPR+A3E',
        #'__utma': '119517141.236589968.1498249286.1500917126.1500921445.5',
        #'__utmz': '119517141.1498249287.1.1.utmcsr=reachlocal|utmccn=search|utmcmd=cpc|utmctr=(not%20provided)',
        #'ASP.NET_SessionId': 'nk1la3jahzxvwtz3a25lx4lk',
        #'ExternalReferrer': '',
        #'rBW-ListingSearch': '21a8d3df-61d2-4115-91da-10a9d216abe2',
        #'BrokerOffice_Visit': '0=c456d055-8967-4b09-910a-f26951a60d28&1=1224-0-0-False',
        #'_gid': 'GA1.2.70223099.1500911588',
        #'MLSLI_tc': '1',
        #'MLSLI_MobilePopup': '1',
        #'__utmc': '119517141',
        #'D_IID': '71FC3A37-EA91-3C28-A5EF-56E4DD48DB63',
        #'D_UID': 'DD4B35DB-2B93-33CF-9D6D-5968DA1BE8C5',
        #'D_ZID': '11613518-1A4C-35B5-8007-6851AAE0565E',
        #'D_ZUID': '2D72399B-3CF4-353F-8FAF-D7A875188928',
        #'D_HID': '266E733E-0819-3C1D-8FCD-5A2885828201',
        #'rBW-CompareListings': '3aa874e4-2930-4b6b-bf61-338b85cb09a5',
        #'PrevSearchSection': 'ListingSearch',
        #'.publicauth': '',
        #'Sml-Login-Action': 'http%253A%252F%252Fwww.mlsli.com%252FListing%252FListingSearch.aspx%25253F%252526search%253D21a8d3df-61d2-4115-91da-10a9d216abe2%252526nextaction%253DSaveSearch',
        #'Sml-Original-Host': 'http%3A%2F%2Fwww.mlsli.com',
        #'Sml-Original-Path': '%2FListing%2FListingSearch.aspx',
        #'rBW-IpLocation': '%257b%2522IPAddressFrom%2522%253a%2522216.223.240.0%2522%252c%2522IPAddressTo%2522%253a%2522216.223.255.255%2522%252c%2522CountryCode%2522%253a%2522US%2522%252c%2522State%2522%253a%2522New%2BYork%2522%252c%2522City%2522%253a%2522Setauket-East%2BSetauket%2522%252c%2522Latitude%2522%253a40.9315%252c%2522Longitude%2522%253a-73.111%252c%2522Timezone%2522%253a%2522America%252fNew_York%2522%252c%2522Pin%2522%253a%257b%2522Lat%2522%253a40.93149948%252c%2522Lon%2522%253a-73.11100006%257d%257d',
        #'_ListingID': '199756112',
        #'__utmb': '119517141.4.10.1500921445',
        #'__utmt': '1',
        #'_gat_adWrapperTracker': '1',
        #'dmp-key': '%2Fdc2%2F_T99%2F3c1043ee-bb65-4b06-9b7c-472c7f9c6bde_M-101164_333359',
        #'scrollposition': '1071',
    }

    headers = {
        'Host': 'www.mlsli.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://www.mlsli.com/Listing/ListingSearch.aspx',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    # proxies = { 'http': '206.127.88.18:80' }
    try:
        r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=8)
        return r
    except:
        return None


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# requests.post('http://www.mlsli.com/Include/AJAX/MapSearch/GetListingPins.aspx?searchoverride=21a8d3df-61d2-4115-91da-10a9d216abe2&ts=1500917583692&', headers=headers, cookies=cookies, data=data)

def scrape_list(conf, proxies):
    dllist = []
    while len(dllist) < 20:
        i = len(dllist)
        prefix = os.path.join('data', 'list', datetime.now().strftime("%Y%m%d_%H%M%S"))
        print(conf)
        if conf['MaxPrice'] < 10000:
            print("skip the low price")
            break
        proxy = next_proxy(proxies)
        r = query_server(conf, {'http': proxy })
        if r is None: # invalid proxy
            proxies[proxy] = -1
            continue

        with open('{}.html'.format(prefix), 'wb') as f:
            f.write(r.content)

        try:
            d = r.json()
        except:
            # proxy is blocked
            proxies[proxy] += 1
            print("proxy {} failed, avail. {}".format(proxy, len(proxies)))
            with open('dead_proxies.txt', 'a') as f:
                f.write("{}\n".format(proxy))
            time.sleep(random.randrange(2,4))
            continue

        if d['pageCount'] == 0:
            logging.warning("pageCount is {}, break".format(d['pageCount']))
            break
        prices = [v['ListPriceLow'] for v in d['ListingResultSet']['Items']]
        logging.debug("prices: {}".format(str(prices)))
        logging.debug("all prices: {} {}".format(min(prices), max(prices)))
        if any([v > conf['MaxPrice'] for v in prices]):
            logging.warning("found a price > MaxPrice({})".format(conf['MaxPrice']))

        with open('{}.json'.format(prefix), 'w') as f:
            f.write(json.dumps(d, indent=4))
        print("{}: {} done".format(i, len(r.content) if r else 0))
        i += 1

        conf['MaxPrice'] = min(prices)
        if d['pageCount'] < conf['ResultsPerPage']:
            logging.debug("{}/{} not filled up, end of search".format(d['pageCount'], conf['ResultsPerPage']))
            break

        if len(proxies) == 0:
            print("No more proxies, quit")
            break

        if next_proxy(proxies) == proxy:
            time.sleep(random.randrange(5, 10))




def scrape_item(conf, url, datadir, proxies, wait=5, cutoff = 10000):
    fpage = '{}/index.html'.format(datadir)
    if os.path.exists(fpage) and os.path.getsize(fpage) > cutoff:
        logging.info("downloaded before, skip {}".format(fpage))
        return fpage

    dllist = []
    while True:
        print(conf)
        proxy = next_proxy(proxies) #
        if not proxy:
            logging.error("can not find valid proxy")
            return None

        logging.info("proxy {} usage: {}".format(proxy, proxies[proxy]))
        r = get_item(url, {'http': proxy })
        if r and len(r.text) > cutoff:
            with open(fpage, 'wb') as f:
                f.write(r.content)
            logging.info("downloaded {} into {}".format(len(r.content), fpage))
            proxies[proxy] += 1
            logging.debug("marking {} = {}".format(proxy, proxies[proxy]))
            time.sleep(random.randrange(3, wait))
            break
        elif not r:
            proxies[proxy] = -1
        else:
            if proxies[proxy] == 0:
                with open('dead_proxies.txt', 'a') as f:
                    f.write("{}\n".format(proxy))
            proxies[proxy] = -1
            logging.debug("proxy: {} failed avail. {}".format(proxy, len(proxies)))
    return fpage
           
# parse_item_list('test_03.html')

with open('dead_proxies.txt', 'r') as f:
    dead = [v.strip() for v in f.readlines()]

with open('proxies.txt', 'r') as f:
    proxies = dict([(v.strip(), 0) for v in f.readlines() if v.strip() not in dead])

if not proxies:
    raise RuntimeError("no proxies found")

logging.info("writting {} good proxies".format(len(proxies)))
with open('proxies.txt', 'w') as f:
    f.write("\n".join(proxies.keys()))

conf = json.load(open('conf.json', 'r'))
print(json.dumps(conf, indent=4))

scrape_list(conf, proxies)

#with open('items.txt', 'r') as f:
#    for url in f.readlines():
#        fdir = url.split('/')[-1].strip()
#        m = re.search("(\d+)-(\d+)$", url)
#        zipcode, lid = m.group(1), m.group(2)
#        datadir = 'data/z{}/{}'.format(zipcode, fdir)
#        os.makedirs(datadir, exist_ok=True)
#        oldidx = 'data/{}__index.html'.format(fdir)
#        if os.path.exists(oldidx):
#            os.rename(oldidx, '{}/index.html'.format(datadir))
#        #    os.rmdir('data/z{}/{}'.format(zipcode, lid))

#        #item = scrape_item(conf, 'http://www.mlsli.com' + url.strip(), datadir, proxies)
#        #if not item:
#        #    break
#    #for k,v in proxies.items():
#    #    print(k, v)


#os.rename('conf.json', 'conf.json.bak')
#with open('conf.json', 'w') as output:
#    json.dump(conf, output)

sys.exit(0)

# time.sleep(5)
#url = 'http://www.mlsli.com/homes-for-sale/Lot-13-Highview-Rd-Stony-Brook-NY-11790-195710143'
#r = get_item(url)
#with open('test.html', 'wb') as f:
#    f.write(r.content)
with open('test.html', 'r') as f:
    text = f.read()
print(len(text))

soup = BeautifulSoup(text, 'html.parser')

for i,p in enumerate(soup.select('#photo-carousel li img')):
    print(i, p['src'])

