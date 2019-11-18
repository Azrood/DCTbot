#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to search on getcomics.info."""

import asyncio
import aiohttp  # lib for going on internet
import urllib.parse
from utils.tools import get_soup_html


async def getcomics_top_link(user_input):
    """Search getcomics and return first result."""
    formated_search = urllib.parse.quote_plus(user_input.lower(),
                                              safe='', encoding=None,
                                              errors=None)
    getcomics_search = f"https://getcomics.info/?s={formated_search}"

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = await get_soup_html(getcomics_search)

    first = soup.find('h1', class_='post-title')

    title = first.text
    url = first.a['href']
    url_dl = await getcomics_directlink(url)
    return title, url_dl


async def getcomics_directlink(comic_url):
    """Get download links in a getcomics post."""
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = await get_soup_html(comic_url)

    direct_download = soup.find('a', class_='aio-red')

    # temp_url is not the final cbz or cbr download url
    temp_url = direct_download['href']

    # We follow temp_url to find final URL
    await asyncio.sleep(1)

    session = aiohttp.ClientSession()

    res2 = await session.get(temp_url, allow_redirects=False, timeout=3, ssl=False)  # noqa:E501
    await session.close()

    if res2.status == 200:
        # print("req 2 code 200")
        return res2.url
    elif res2.status == 302:
        # print("302, Found Comic URL")
        return res2.headers['location']
    elif res2.status == 404:
        # print('404, returning post url')
        # in this case, return the getcomics post url
        return comic_url
    else:
        # in this case, return the getcomics post url
        # print("unkwnown response code")
        return comic_url
