import os
import re
import sys
import shutil
import json
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import random
import operator
import glob

import requests

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

cols = ('ListPriceLow', 'SoldPrice', 'NumberBedrooms', 'NumberBaths', 'PostalCode', 'ListingNumber', 'ListFile', 'url')

def parse_listing_html(lsthtml):
    soup = BeautifulSoup(lsthtml, 'html.parser')
    prptList = {}
    for i,p in enumerate(soup.find_all('div', 'listview-result')):
        #print(i, "=========================")
        #if i == 0:
        #    print(i, p.prettify())
        r = dict([(c, '_') for c in cols])
        m = re.search('MLS:\s*([\d]+)', p.text)
        r['MLS'] = m.group(1) if m else '0'
        data = p.find('div', class_='listview-photocontainer').find('div', class_='ratings-widget')
        if data:
            r['MLS'] = data['data-listingnumber'] # may have P12.....
            r['ListingID'] = int(data['data-listingid'])
        
        for price in p.select('.listview-price'):
            # print(price.prettify())
            r['url'] = price.find('a')['href']
            m = re.search('(Sold|Active)', price.text)
            r['Sold'] = 1 if m else 0
            m = re.search('\$([\d,]+)', price.text)
            if m:
                # logging.info("found Sold={} price: {} ({})".format(r['Sold'], m.group(1), r.get('ListingID', '')))
                r['Price'] = int(m.group(1).replace(',', ''))
        prptList[r['ListingID']] = r
    return prptList


allList = {}
# read list
for s in open('data/list.txt', 'r'):
    if not s.strip(): continue
    r = dict(zip(cols, s.split()))
    r['ListPriceLow'] = int(r['ListPriceLow'])
    r['SoldPrice'] = int(r['SoldPrice'])
    kk = (r['ListingNumber'], r['ListPriceLow'], r['SoldPrice'])
    allList.setdefault(kk, r)

output = open("data/list.txt.tmp", 'w')
for f in sorted(sys.argv[1:]):
    d = json.load(open(f, 'r'))
    # print (json.dumps(d, indent=4))
    #print(json.dumps(d['lst'][0], indent=4))
    #print(json.dumps(d['ListingResultSet']['Items'][0], indent=4))
    #print(d.keys())
    pagePrpt = parse_listing_html(d['listingsHtml'])
    # print(pagePrpt)
    if len(d['lst']) != len(d['ListingResultSet']['Items']):
        # raise RuntimeError("list items not same size: {} {} in {}".format(len(d['lst']), len(d['ListingResultSet']['Items']), f))
        logging.warning("list items not same size: {} {} in {}".format(len(d['lst']), len(d['ListingResultSet']['Items']), f))
    #for r1,r2 in zip(d['lst'], d['ListingResultSet']['Items']):
    r = {}
    for r1 in d['lst']:
        r.setdefault(r1['lid'], {'url': r1['url']})
        if r1['lid'] in pagePrpt:
            # logging.debug("setting sold price {} = {}, sold= {}".format(r1['lid'], pagePrpt[r1['lid']]['Price'], pagePrpt[r1['lid']].get('Sold', 0) ))
            if pagePrpt[r1['lid']].get('Sold', 0):
                r[r1['lid']].setdefault('SoldPrice', pagePrpt[r1['lid']]['Price'])
        else:
            # logging.debug('{} ({}) not in listingHtml'.format(r1['lid'], type(r1['lid'])))
            pass
            
    for r2 in d['ListingResultSet']['Items']:
        r.setdefault(r2['ListingID'], {}) # should already set with d['lst']
        for k in cols:
            if k not in r2: continue
            r[r2['ListingID']][k] = r2[k]
    # print(r)
    for k,v in r.items():
        v.setdefault('SoldPrice', 0)
        v.setdefault('ListFile', os.path.basename(f.strip()))
        if any([c not in v for c in cols]):
            continue
        output.write(' '.join(['{}'.format(v[c]) for c in cols]) + '\n')
        kk = (v['ListingNumber'], v['ListPriceLow'], v['SoldPrice'])
        allList.setdefault(kk, dict([(c, v[c]) for c in cols]))

output.close()
t = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copyfile("data/list.txt", "data/list/{}.txt".format(t))

f = open('data/list.txt', 'w')
for k,v in sorted(allList.items(), key=lambda kv: kv[1]['ListPriceLow'], reverse=True):
    f.write(" ".join(["{}".format(v[c]) for c in cols]) + "\n")
f.close()


