#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""Some functions to parse forum using bs4."""

import re
from dataclasses import dataclass
from string import ascii_uppercase
from typing import List

import aiohttp


@dataclass
class TopicOrForum:
    """Class for topic information."""
    name: str
    url: str

    def __lt__(self, other: 'TopicOrForum') -> bool:
        return self.name < other.name


def get_sub_forums(htmlsoup) -> List[TopicOrForum]:
    if sub_forums := htmlsoup.select("a.forumtitle"):
        return [TopicOrForum(name=s.text, url=s['href']) for s in sub_forums]
    return []


def get_topics(htmlsoup) -> List[TopicOrForum]:
    if topics := htmlsoup.select("a.topictitle"):
        return [TopicOrForum(name=t.text, url=t['href']) for t in topics]
    return []


def get_nb_topics(htmlsoup) -> int:
    """Get number of topics in sub-forum."""
    try:
        raw = htmlsoup.select('div.pagination')[0].text
        n = re.search(r"(?P<nb_topics>\d+?) sujet(s)?", raw)['nb_topics']
        return int(n)
    except (AttributeError, TypeError):
        return 0


async def get_all_topics(phpbb, html, url) -> List[TopicOrForum]:
    # First iteration, we allready have the html from the while loop
    n: int = get_nb_topics(html)
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
    return sorted(topics)


def print_res_numbers(res_list, start_index=0) -> None:
    if res_list:
        for i, res in enumerate(res_list, start_index):
            print(f"{i:.<5d}{res['name']:.<20s}{res['url']}")


def print_res_letters(res_list, start_index=0) -> None:
    if res_list:
        for i, res in enumerate(res_list, start_index):
            print(f"{ascii_uppercase[i]:.<5s}{res['name']:.<20s}{res['url']}")
