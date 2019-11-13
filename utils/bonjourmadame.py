#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Bonjourmadame feed parser."""

import aiohttp
from bs4 import BeautifulSoup


async def latest_madame():
    """Fetch last Bonjourmadame picture."""
    madames = "http://feeds2.feedburner.com/BonjourMadame"
    async with aiohttp.ClientSession as session:
        async with session.get(madames) as resp:
            text = resp.text()
        await session.close()
    soup = BeautifulSoup(text, 'lxml')
    item = soup.find('item')
    url = item.find('img')['src']

    return url.split('?')[0]
