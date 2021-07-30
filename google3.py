#!/usr/bin/env python
# coding=utf-8
import requests
import proxybroker
import sys
import sys

from skimage.util.tests.test_arraypad import ValueError3
from termcolor import colored, cprint
import warnings
import random
from http import cookiejar
import os
import time
import asyncio
from proxybroker import Broker
from bs4 import BeautifulSoup as bs
import threading
from urllib.parse import quote_plus, urlparse, parse_qs
from requests.exceptions import HTTPError


__author__ = "isabostan@gmail.com"

READ_FILENAME = 'keywrd.txt'
WRITE_FILENAME = 'result.txt'


# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s&" \
             "cr=%(country)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s&" \
                "cr=%(country)s"
url_search_num = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                 "num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
                 "tbm=%(tpe)s&cr=%(country)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&tbm=%(tpe)s&cr=%(country)s"
url_parameters = (
    'hl', 'q', 'num', 'btnG', 'start', 'tbs', 'safe', 'tbm', 'cr')

TLD = ["com","com.tw","co.in","be","de","co.uk","co.ma","dz","ru","ca","ws","sr","tk","sc","nu","ms","me","la","gg","fm","dj","cd","as","ad","com.tr"]

headers={
    "User-Agent" : "Mozilla / 5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.84 Safari / 537.36"
 }
USER_AGENT = 'Mozilla / 5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 63.0.3239.84 Safari / 537.36'
thread_count = 1
proxy_list = []
async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        proxy_list.append(proxy)
        print('Found proxy: %s' % proxy)

def get_proxies():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=50), show(proxies)
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False
#class gSearch():
class gSearch(threading.Thread):
    def __init__(self,w_thread, prxy_list, query, tld):
        threading.Thread.__init__(self)
        #self.get_proxy_list(list(prxy_list))
        self.w_thread = w_thread
        self.prxy = prxy_list
        self.query = query
        self.tld = tld
        beta = random.choice(TLD)
        print(self.prxy)

    # Filter links found in the Google result pages HTML code.
    # Returns None if the link doesn't yield a valid result.
    def filter_result(self,link):
        try:

            # Decode hidden URLs.
            if link.startswith('/url?'):
                o = urlparse(link, 'http')
                link = parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain,
            # like images.google.com or googleusercontent.com for example.
            # TODO this could be improved!
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

        # On error, return None.
        except HTTPError as hx:
            print("http err:",hx)

    def search(self,query, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, domains=None, pause=2.0, tpe='', country='',
           extra_params=None, user_agent=None):
        try:
            # Set of hashes for the results found.
            # This is used to avoid repeated results.
            s = requests.Session()
            s.cookies.set_policy(BlockAll())
            beta = random.choice(TLD)
            time.sleep(3)

            hashes = set()
            tld = tld
            lang = lang
            tbs=tbs
            safe=safe
            num=num
            start=start
            stop=stop
            domains = domains
            pause = pause
            tpe = tpe
            country = country
            extra_params = extra_params
            user_agent = user_agent

            # Count the number of links yielded.
            count = 0

            # Prepare domain list if it exists.
            if domains:
                query = query + ' ' + ' OR '.join(
                    'site:' + domain for domain in domains)

            # Prepare the search string.
            query = quote_plus(query)

            # If no extra_params is given, create an empty dictionary.
            # We should avoid using an empty dictionary as a default value
            # in a function parameter in Python.
            if not extra_params:
                extra_params = {}

            # Check extra_params for overlapping.
            for builtin_param in url_parameters:
                if builtin_param in extra_params.keys():
                    raise ValueError(
                        'GET parameter "%s" is overlapping with \
                        the built-in GET parameter',
                        builtin_param
                    )

            # Grab the cookie from the home page.
            print(url_home%vars())
            print("home")

            self.get_page(url=url_home%vars(), user_agent=user_agent,proxies=self.prxy)

            # Prepare the URL of the first request.
            if start:
                if num == 10:
                    url = url_next_page % vars()
                else:
                    url = url_next_page_num % vars()
            else:
                if num == 10:
                    url = url_search % vars()
                else:
                    url = url_search_num % vars()

            # Loop until we reach the maximum result, if any (otherwise, loop forever).
            while not stop or count < stop:

                # Remeber last count to detect the end of results.
                last_count = count

                # Append extra GET parameters to the URL.
                # This is done on every iteration because we're
                # rebuilding the entire URL at the end of this loop.
                for k, v in extra_params.items():
                    k = quote_plus(k)
                    v = quote_plus(v)
                    url = url + ('&%s=%s' % (k, v))

                print(url)
                print("url---")
                # Sleep between requests.
                # Keeps Google from banning you for making too many requests.
                time.sleep(pause)

                # Request the Google Search results page.
                #html = self.get_page(url=url%vars(), user_agent=user_agent, proxies=self.prxy)
                html = self.get_page(url=url, user_agent=user_agent, proxies=self.prxy)
                # Parse the response and get every anchored URL.
                #if is_bs4:

                soup = bs(html, 'html.parser')
                #else:
                #    soup = BeautifulSoup(html)
                try:
                    anchors = soup.find(id='search').findAll('a')
                    # Sometimes (depending on the User-agent) there is
                    # no id "search" in html response...
                except AttributeError:
                    # Remove links of the top bar.
                    gbar = soup.find(id='gbar')
                    if gbar:
                        gbar.clear()
                    anchors = soup.findAll('a')

                # Process every anchored URL.
                for a in anchors:

                    # Get the URL from the anchor tag.
                    try:
                        link = a['href']
                    except KeyError:
                        continue

                    # Filter invalid links and links pointing to Google itself.
                    link = self.filter_result(link)
                    if not link:
                        continue

                    # Discard repeated results.
                    h = hash(link)
                    if h in hashes:
                        continue
                    hashes.add(h)

                    with open(WRITE_FILENAME,"a+") as wf:
                        wf.write(str(link)+"\n")
                    # Yield the result.
                    yield link


                    # Increase the results counter.
                    # If we reached the limit, stop.
                    count += 1
                    if stop and count >= stop:
                        return

                # End if there are no more results.
                # XXX TODO review this logic, not sure if this is still true!
                if last_count == count:
                    break

                # Prepare the URL for the next request.
                start += num
                if num == 10:
                    url = url_next_page % vars()
                else:
                    url = url_next_page_num % vars()
        except ValueError as hx:
            print("search http err:",hx)

    # Request the given URL and return the response page, using the cookie jar.
    # If the cookie jar is inaccessible, the errors are ignored.
    def get_page(self,url, user_agent=None,proxies=None):
        """
        Request the given URL and return the response page, using the cookie jar.

        :param str url: URL to retrieve.
        :param str user_agent: User agent for the HTTP requests.
            Use None for the default.

        :rtype: str
        :return: Web page retrieved for the given URL.

        :raises IOError: An exception is raised on error.
        :raises urllib2.URLError: An exception is raised on error.
        :raises urllib2.HTTPError: An exception is raised on error.
        """
        print("url get:",url)
        if user_agent is None:
            user_agent = headers
        r = requests.get(url, headers=user_agent)
        print(r.status_code)
        if r.status_code == 200:
            html = r.text
        else:
            html = None
        return html

    def get_proxy_list(self,prxlst):
        if len(prxlst):
            for p in prxlst:
                print(p)
                if "[HTTP: High, HTTPS]" in str(p):
                    p1 = str(p).split("[HTTP: High, HTTPS]")[1].strip().split(">")[0].strip()
                    self.prxy = p1
                    break
            print(self.prxy)
        else:
            print("Proxy list is empty,try later")
            exit()
    def run(self):
        try:
            tld = self.tld
            query = self.query
            for s1, gamma in enumerate(self.search(query=query, tld=tld, num=10, stop=95, pause=2,user_agent=headers)):
                print(s1,gamma)
        except HTTPError as hx:
            print("run http err:",hx)

thrds = []
def main(proxy_list):
    try:
        prx = []
        if len(proxy_list):
            for p in proxy_list:
                #print(p)
                if "[HTTP: High, HTTPS]" in str(p):
                    p1 = str(p).split("[HTTP: High, HTTPS]")[1].strip().split(">")[0].strip()
                    prx.append(p1)
                    #break
            print(len(prx))
            if len(prx):
                thread_count = len(prx)
            else:
                thread_count = 0
                print("There is no proxy, try again later")
                exit()
        q_list = []
        with open(READ_FILENAME,"r",encoding="utf-8") as rf:
            for r in rf.readlines():
                q_list.append(r)
        for tld in TLD:
            for s,p in enumerate(prx):
                p_data = {"http":str(p),"https":str(p)}
                t = gSearch(w_thread=s,prxy_list=p_data,query=q_list[s],tld=tld)
                print("Starting: --- " + str(s) + " --- from main")
                t.setDaemon(True)
                thrds.append(t)
                t.start()
                time.sleep(2)
                # time.sleep(1)
            for t in thrds:
                t.join()



    except:
        pass


if __name__ == "__main__":
    with open(WRITE_FILENAME,"w") as wf:
        pass
    get_proxies()
    main(proxy_list)
    #gSearch(0,list(proxy_list),"inurl:index.php?id=",None)
    #print(proxy_list)