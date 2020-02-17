"""File for some tools."""

import aiohttp  # asynchronous lib for going on internet

from bs4 import BeautifulSoup
# from discord.utils import get as disc_get
from discord.utils import find as disc_find


def string_is_int(string):  # pragma: no cover
    """Return if 'string' is an int or not (bool)."""
    try:
        int(string)
        return True
    except ValueError:
        return False


async def get_soup_lxml(url):
    """Return a BeautifulSoup soup from given url, Parser is lxml.

    Args:
        url (str): url

    Returns:
        BeautifulSoup: soup

    """
    # get HTML page with async GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=3, ssl=False) as resp:
            text = await resp.text()
        await session.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    return BeautifulSoup(text, 'lxml')


async def get_soup_html(url):
    """Return a BeautifulSoup soup from given url, Parser is html.parser.

    Args:
        url (str): url

    Returns:
        BeautifulSoup: soup

    """
    # get HTML page with async GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=3, ssl=False) as resp:
            text = await resp.text()
        await session.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    return BeautifulSoup(text, 'html.parser')


def args_separator_for_log_function(guild, args):
    """Check the args if there are user, channel and command."""
    commands = ['kick', 'clear', 'ban']
    [user, command, channel] = [None, None, None]  # They are defaulted to None, if any of them is specified, it will be changed  # noqa:E501
    for word in args:
        # if disc_get(guild.members, name=word) is not None: # if word is a member of the guild  # noqa:E501
        if disc_find(lambda m: m.name.lower() == word.lower(), guild.members) is not None:  # same, but case insensitive  # noqa:E501
            user = word.lower()
        # elif disc_get(guild.text_channels, name=word) is not None: # if word is a channel of the guild  # noqa:E501
        elif disc_find(lambda t: t.name.lower() == word.lower(), guild.text_channels) is not None:  # same, but case insensitive  # noqa:E501
            channel = word.lower()
        elif word in commands:  # if word is a command
            command = word.lower()
    # variables not specified in the args are defaulted to None
    return [user, command, channel]
