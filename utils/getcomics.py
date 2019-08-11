#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import requests  # lib for going on internet
from bs4 import BeautifulSoup  # html parser
import urllib.parse


def getcomics_top_link(user_input):

    formated_search = urllib.parse.quote_plus(user_input.lower(),
                                              safe='', encoding=None,
                                              errors=None)
    getcomics_search = f"https://getcomics.info/?s={formated_search}"
    # get HTML page with requests.get
    res = requests.get(getcomics_search)
    res.close()

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = BeautifulSoup(res.text, 'lxml')

    first = soup.find('h1', class_='post-title')

    title = first.text
    url = first.a['href']
    url_dl = getcomics_directlink(url)
    return title, url_dl


def getcomics_directlink(comic_url):

    # get HTML page with requests.get
    res = requests.get(comic_url)
    res.close()

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = BeautifulSoup(res.text, 'html.parser')

    direct_download = soup.find('a', class_='aio-red')

    # temp_url is not the final cbz or cbr download url
    temp_url = direct_download['href']

    # We follow temp_url to find final URL
    time.sleep(2)

    res2 = requests.get(temp_url, allow_redirects=False, stream=True)
    res2.close()

    if res2.status_code == 200:
        print("req 2 code 200")
        print(res2.url)
    elif res2.status_code == 302:
        print("302, Found Comic URL")
        return res2.headers['location']
    elif res2.status_code == 404:
        print('404, returning post url')
        # in this case, return the getcomics post url
        return comic_url
    else:
        # in this case, return the getcomics post url
        print("unkwnown response code")
        return comic_url
