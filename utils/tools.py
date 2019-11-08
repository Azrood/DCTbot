"""File for some tools."""

import requests  # lib for going on internet
from bs4 import BeautifulSoup
from discord.utils import get as disc_get


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

def args_separator_for_log_function(guild,args):
    """check the args if there are user, channel and command""" 
    commands = ['kick','clear','ban']
    [user,command,channel] = [None,None,None] # They are defaulted to None, if any of them is specified, it will be changed
    for word in args:
        if disc_get(guild.members, name=word) is not None: # if word is a member of the guild
            user = word
        elif disc_get(guild.text_channels, name=word) is not None: # if word is a channel of the guild
            channel = word
        elif word in commands: # if word is a command
            command = word
    return [user, command, channel] # variables not specified in the args are defaulted to None
    