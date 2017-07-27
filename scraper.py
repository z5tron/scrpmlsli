#!/usr/bin/python3

import re
import sys
import json
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import random

import requests

def query_server(itemFirst, proxies, maxprice='', rpp=40):
    
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
        ('Criteria/MaxPrice', maxprice),
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
         ('first', itemFirst),
        ('Criteria/SearchType', 'map'),
        ('SearchTab', 'mapsearch-criteria-basicsearch'),
        ('CLSID', '-1'),
        ('ResultsPerPage', rpp), # default was 10
    ]
    print(proxies)
    try:
        r = requests.post('http://www.mlsli.com/Include/AJAX/MapSearch/GetListingPins.aspx', headers=headers, params=params, cookies=cookies, data=data, proxies=proxies, timeout=8)
        #r = requests.post('http://www.baidu.com/', proxies=proxies)
        return r
    except:
        return None

def get_item(url):
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
    proxies = { 'http': '206.127.88.18:80' }
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    return r


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# requests.post('http://www.mlsli.com/Include/AJAX/MapSearch/GetListingPins.aspx?searchoverride=21a8d3df-61d2-4115-91da-10a9d216abe2&ts=1500917583692&', headers=headers, cookies=cookies, data=data)

def scrape(proxies, i = 0, maxprice = ''):
    rpp = 40
    while i < 20:
        print("maxprice=", maxprice, " rpp=", rpp)
        proxy = proxies[i % len(proxies)].split()[0].strip()
        r = query_server(0, {'http': proxy }, maxprice, rpp)
        try:
            #with open('test_m{:02d}.html'.format(i), 'wb') as f:
            #    f.write(r.content)
            d = r.json()
            if d['pageCount'] == 0:
                break
            prices = [v['ListPriceLow'] for v in d['ListingResultSet']['Items']]
            if any([v > maxprice for v in prices]):
                break
            with open('test_m{:02d}.json'.format(i), 'w') as f:
                f.write(json.dumps(d, indent=4))
            print("{}: {} done".format(i, len(r.content) if r else 0))
            i += 1

            maxprice = min(prices)
            if d['pageCount'] < rpp:
                maxprice -= 1

            time.sleep(random.randrange(5, 10))
        except:
            proxies.pop(i)
            print("proxy {} failed, avail. {}".format(proxy, len(proxies)))
            with open('dead_proxies.txt', 'a') as f:
                f.write("{}\n".format(proxy))
            time.sleep(random.randrange(3,8))
        if len(proxies) == 0:
            print("No more proxies, quit")
            break


def parse_item_list(flist):
    # its a JSON format
    with open(flist, 'r') as f:
        d = json.loads(f.read())
        json.dumps(d, indent=4)

    soup = BeautifulSoup(d['listingsHtml'], 'html.parser')
    prptList = {}
    for i,p in enumerate(soup.find_all('div', 'listview-result')):
        print(i, "=========================")
        if i == 0:
            print(i, p.prettify())
        url, sold, price, mls, lis = None, None, None, None, None
        m = re.search('MLS:\s*([\d]+)', p.text)
        mls = m.group(1) if m else ''
        data = p.find('div', class_='listview-photocontainer').find('div', class_='ratings-widget')
        if data:
            mls = data['data-listingnumber']
            lid = data['data-listingid']
        
        for price in p.select('.listview-price'):
            # print(price.prettify())
            url = price.find('a')['href']
            m = re.search('(Sold|Active)', price.text)
            sold = True if m else False # : print(m.group(0), end=', ')
            m = re.search('\$[\d,]+', price.text)
        prptList[url] = { 'sold': sold,
                          'price': m.group(0),
                          'mls': mls,
                          'lid': lid}
    print(prptList)

    #print(d['lst'])

# parse_item_list('test_03.html')

with open('proxies.txt', 'r') as f:
    proxies = f.readlines()

maxprice='199000'
scrape(proxies, 15, maxprice)
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

