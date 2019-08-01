#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests  # lib for going on internet
from bs4 import BeautifulSoup  # html parser
def get_top_def(user_input):

    urban_url = "https://www.urbandictionary.com/define.php?term={}"

    # Make the search url : www.urbandictionary.com/define.php?term=taco+hole
    search_url = urban_url.format(user_input.lower().replace(' ', '+'))

    # print(search_url)

    # get HTML page with requests.get
    res = requests.get(search_url)
    res.close()

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = BeautifulSoup(res.text, 'lxml')

    # unquote this if you want to see what is a "soup"
    # print(soup.prettify())

    # parse the HTML soup to find Top Definition title, meaning, example
    title = soup.select_one('div.def-panel > div.def-header > a.word').text
    meaning = soup.select_one('div.def-panel > div.meaning').text
    example = soup.select_one('div.def-panel > div.example').text

    return title,meaning,example,search_url