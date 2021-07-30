

'''import requests
import re
import time
from bs4 import BeautifulSoup as bs

Headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}

data = {
    "q":"inurl:index.php?id="
}

#base_url = "https://www.google.com/search?"
start = time.time()
#r = requests.get(base_url,params=data,headers = Headers)
#print(r.status_code)
#print(r.url)
#print(r.text)
rurl = "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=10&cad=rja&uact=8&ved=2ahUKEwjhgPz75I7pAhWvwMQBHRY5AkoQFjAJegQIChAB&url=http%3A%2F%2Fwww.epomm.eu%2Fmaxeva%2Findex.php%3Fid%3D1&usg=AOvVaw0zcTWE9huITd1HsLoY037r"
tmpPage = requests.get(rurl, allow_redirects=False)
#print(tmpPage.status_code)
#print(tmpPage.text)
#print(tmpPage.url)
if tmpPage.status_code == 200:
    sp = bs(tmpPage.text,"html.parser")
    print(sp.find("meta").get("content"))
    #print(dir(sp.find("meta")))
    #urlMatch = re.search(r'url=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
    #print("whatisthis:",(urlMatch.group(1), tmpPage))
#elif tmpPage.status_code == 302:
#    print((tmpPage.headers.get('location'), tmpPage))
    #is_there = [x for x in self.exclude_items.split("|") if x in str(tmpPage.headers.get('location'))]
    #if not tmpPage.headers.get('location') in self.links and len(is_there)==0:
        #with open(self.output, 'a+') as fd:
        #    fd.write(tmpPage.headers.get('location') + '\n')
    #self.links.append(tmpPage.headers.get('location'))
#else:
#    print('No URL found!  !')
print("time spent:",time.time()-start)
#----------
from urllib import request
from urllib.parse import urlencode
from urllib.request import urlopen
import json


URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
recaptchaResponse = request.get('recaptchaResponse', None)
private_recaptcha = '6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b'
remote_ip = request.remote_addr
params = urlencode({
    'secret': private_recaptcha,
    'response': recaptchaResponse,
    'remote_ip': remote_ip,
})

# print params
data = urlopen(URIReCaptcha, params.encode('utf-8')).read()
result = json.loads(data)
success = result.get('success', None)

if success == True:
    print('reCaptcha passed')
else:
    print('recaptcha failed')
'''

headers={
    "User-Agent" : "Mozilla / 5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.84 Safari / 537.36"
 }
#
# import asyncio
# from proxybroker import Broker
# from termcolor import colored, cprint
# import sys
# import os
#
# async def show(proxies):
#     while True:
#         proxy = await proxies.get()
#         if proxy is None:
#             break
#         print('Found proxy: %s' % proxy)
#
#
# proxies = asyncio.Queue()
# broker = Broker(proxies)
# tasks = asyncio.gather(
#     broker.find(types=['HTTP', 'HTTPS'], limit=25 ), show(proxies)
# )
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tasks)
# print(colored('[+] Done', 'green'))
url = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s"
tld = "com"
lang = "en"
query = "hello"
print(url%vars())