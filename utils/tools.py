"""File for some tools."""

import requests  # lib for going on internet
from bs4 import BeautifulSoup


def string_is_int(string):
    """Return if 'string' is an int or not (bool)."""
    try:
        int(string)
        return True
    except ValueError:
        return False


def get_soup_lxml(url):
    """Return a BeautifulSoup soup from given url, Parser is lxml.

    Args:
        url (str): url

    Returns:
        BeautifulSoup: soup

    """
    # get HTML page with requests.get
    res = requests.get(url, timeout=3)
    res.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    return BeautifulSoup(res.text, 'lxml')


def get_soup_html(url):
    """Return a BeautifulSoup soup from given url, Parser is html.parser.

    Args:
        url (str): url

    Returns:
        BeautifulSoup: soup

    """
    # get HTML page with requests.get
    res = requests.get(url, timeout=3)
    res.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    return BeautifulSoup(res.text, 'html.parser')
