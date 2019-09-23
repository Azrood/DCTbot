#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.parse import quote_plus

from utils.tools import get_soup_lxml


# Class to make request on Urban Dictionary
class Urban_search:
    urban_url = "https://www.urbandictionary.com/define.php?term="

    # init is executed when the object is created
    def __init__(self, user_input):
        formated_input = quote_plus(user_input.lower())

        # Make search url: www.urbandictionary.com/define.php?term=distro+hop
        self.search_url = self.urban_url + formated_input
        self.soup = get_soup_lxml(self.search_url)
        self.isokay()

    # Test if the page is a definition, or is dummy
    def isokay(self):
        # Test if I can find the div for :
        # Sorry, we couldn't find XXX
        # If not, search is valid
        if self.soup.select_one('div.term.space'):
            self.valid = False
        else:
            self.valid = True

    def get_top_def(self):
        # parse the HTML soup to find Top Definition title, meaning, example
        title = self.soup.select_one('div.def-panel > div.def-header > a.word').text
        meaning = self.soup.select_one('div.def-panel > div.meaning').text
        example_raw = self.soup.select_one('div.def-panel > div.example').text
        if hasattr(example_raw, 'text'):
            example = example_raw.text
        else:
            example = "No example"
        return title, meaning, example, self.search_url
