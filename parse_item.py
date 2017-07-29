#!/usr/bin/python3

import aiohttp
import asyncio
import async_timeout

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

async def download_coroutine(session, url, datadir):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            filename = os.path.join(datadir, os.path.basename(url))
            with open(filename, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
            return await response.release()
 
 
async def main(loop, urls, datadir):
 
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url, datadir) for url in urls]
        await asyncio.gather(*tasks)
 

if __name__ == '__main__':
    for fpage in open('pages.txt', 'r').readlines():
        fpage = fpage.strip()
        datadir = fpage.replace("/index.html", "")
        print(datadir)
        text = open(fpage, 'r', errors='ignore').read()
        soup = BeautifulSoup(text, 'html.parser')

        pics = []
        for i,p in enumerate(soup.select('#photo-carousel li img')):
            if os.path.exists(datadir + '/' + os.path.basename(p['src'])): continue
            print("  ", i, p['src'])
            pics.append(p['src'])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop, pics, datadir))
        time.sleep(3)
        
