#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""Some functions to parse forum using bs4."""

import re
from operator import itemgetter
from string import ascii_uppercase

import aiohttp


def get_sub_forums(html):
    sub_forums = html.select("a.forumtitle")
    if sub_forums:
        return [{'name': s.text, 'url': s['href']} for s in sub_forums]
    return []


def get_nb_topics(html):
    """Get number of topics in sub-forum."""
    try:
        raw = html.select('div.pagination')[0].text
        n = re.search(r"(?P<nb_topics>\d+?) sujet(s)?", raw).group('nb_topics')
        return int(n)
    except AttributeError:
        return 0


def get_topics(html):
    topics = html.select("a.topictitle")
    if topics:
        return [{'name': t.text, 'url': t['href']} for t in topics]
    return []


async def get_all_topics(phpbb, html, url):
    # First iteration, we allready have the html from the while loop
    n = get_nb_topics(html)
    topics = get_topics(html)
    n -= 40
    start = 40
    while n > 0:
        params = {'start': start}
        try:
            html = await phpbb.browser.get_html(url, params=params)
        except aiohttp.client_exceptions.ServerDisconnectedError:
            continue
        new_topics = get_topics(html)
        topics += new_topics
        n -= 40
        start += 40
    sorted_topics = sorted(topics, key=itemgetter('name'))
    return sorted_topics


def print_res_numbers(res_list, start_index=0):
    if res_list:
        for i, res in enumerate(res_list, start_index):
            # print(i, res['name'], res['url'])
            print(f"{i:.<5d}{res['name']:.<20s}{res['url']}")


def print_res_letters(res_list, start_index=0):
    if res_list:
        for i, res in enumerate(res_list, start_index):
            # print(i, res['name'], res['url'])
            print(f"{ascii_uppercase[i]:.<5s}{res['name']:.<20s}{res['url']}")
