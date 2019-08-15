#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import requests  # lib for going on internet
import urllib.parse
from utils.tools import get_soup_html


def getcomics_top_link(user_input):

    formated_search = urllib.parse.quote_plus(user_input.lower(),
                                              safe='', encoding=None,
                                              errors=None)
    getcomics_search = f"https://getcomics.info/?s={formated_search}"

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = get_soup_html(getcomics_search)

    first = soup.find('h1', class_='post-title')

    title = first.text
    url = first.a['href']
    url_dl = getcomics_directlink(url)
    return title, url_dl


def getcomics_directlink(comic_url):

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = get_soup_html(comic_url)

    direct_download = soup.find('a', class_='aio-red')

    # temp_url is not the final cbz or cbr download url
    temp_url = direct_download['href']

    # We follow temp_url to find final URL
    time.sleep(1)

    res2 = requests.get(temp_url, allow_redirects=False, stream=True, timeout=3)
    res2.close()

    if res2.status_code == 200:
        print("req 2 code 200")
        return res2.url
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
