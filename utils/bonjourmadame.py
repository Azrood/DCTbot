#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Bonjourmadame feed parser."""

import requests
from bs4 import BeautifulSoup


def latest_madame():
    """Fetch last Bonjourmadame picture."""
    madames = "http://feeds2.feedburner.com/BonjourMadame"

    res = requests.get(madames)
    res.close()
    soup = BeautifulSoup(res.text, 'lxml')

    item = soup.find('item')
    url = item.find('img')['src']

    return url.split('?')[0]
