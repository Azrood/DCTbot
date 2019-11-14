#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to search on urban dictionary."""
import aiohttp

from urllib.parse import quote_plus
from utils.tools import get_soup_lxml


# Class to make request on Urban Dictionary
class UrbanSearch:
    """Class to search on urban dictionary."""

    urban_url = "https://www.urbandictionary.com/define.php?term="

    def __init__(self, user_input):
        """Init object with user input, search, and get lxml soup."""
        formated_input = quote_plus(user_input.lower())

        # Make search url: www.urbandictionary.com/define.php?term=distro+hop
        self.search_url = self.urban_url + formated_input
        self.soup = None
        self.valid = False

    def _isokay(self):
        """Test if the page is a definition, or is dummy."""
        # Test if I can find the div for :
        # Sorry, we couldn't find XXX
        # If not, search is valid
        if self.soup.select_one('div.term.space'):
            self.valid = False
        else:
            self.valid = True

    async def fetch(self):
        self.soup = await get_soup_lxml(self.search_url)
        self._isokay()

    def get_top_def(self):
        """Parse the HTML soup to find Top Definition title, meaning, example."""  # noqa:E501
        title = self.soup.select_one('div.def-panel > div.def-header > a.word').text  # noqa:E501
        meaning = self.soup.select_one('div.def-panel > div.meaning').text
        example_raw = self.soup.select_one('div.def-panel > div.example').text
        if hasattr(example_raw, 'text'):
            example = example_raw.text
        else:
            example = "No example"
        return title, meaning, example, self.search_url
