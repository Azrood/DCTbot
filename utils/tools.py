# File for some tools

import requests  # lib for going on internet
from bs4 import BeautifulSoup


def get_command_input(user_input):
    return user_input.split(' ', 1)[1]


def string_is_int(string):
    try:
        a = int(string)
        return True
    except ValueError:
        return False


def get_soup_lxml(url):
    # get HTML page with requests.get
    res = requests.get(url)
    res.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    return BeautifulSoup(res.text, 'lxml')
