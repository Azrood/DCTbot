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

def args_separator_for_log_function(users,chans,args):
    """check the args if there are user, channel and command""" 
    commands = ['kick','clear','ban']
    f1,f2,f3 = False,False,False
    returned_list=[] # in format [user,command,chan]
    liste = args.split()
    for word in liste:
        if word in users:
            f1 = True
            user = word
        elif word in commands:
            f2 = True
            command = word
        elif word in chans:
            f3 = True
            channel = word
    if f1:
        returned_list.append(user)
    else:
        returned_list.append(None)
    if f2:
        returned_list.append(command)
    else:
        returned_list.append(None)
    if f3:
        returned_list.append(channel)
    else:
        returned_list.append(None)

    return returned_list
        