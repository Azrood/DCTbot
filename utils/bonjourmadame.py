#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Bonjourmadame feed parser."""

from utils.tools import get_soup_lxml


async def latest_madame():
    """Fetch last Bonjourmadame picture."""
    madames = "http://feeds2.feedburner.com/BonjourMadame"
    soup = await get_soup_lxml(madames)
    item = soup.find('item')
    url = item.find('img')['src']

    return url.split('?')[0]
