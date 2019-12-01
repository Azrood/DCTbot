#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Urban dictionnary cog."""

from urllib.parse import quote_plus
from utils.tools import get_soup_lxml

import discord
from discord.ext import commands

urban_logo = "https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg"  # noqa: E501


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


class Urban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *, user_input):
        """Send definition of user input on Urban Dictionary."""
        # create object urban of class Urban
        urban = UrbanSearch(user_input)
        await urban.fetch()
        if urban.valid:
            title, meaning, example, search_url = urban.get_top_def()
            embed = discord.Embed(title=f"Definition of {title[:100]}",
                                  description=meaning[:2048], color=0x00FFFF,
                                  url=search_url)
            embed.add_field(name="Example", value=example[:2048], inline=False)
            embed.set_thumbnail(url=urban_logo)
        else:
            embed = discord.Embed(title=f"Definition of {user_input} doesn't exist")  # noqa: E501
        await ctx.send(embed=embed)
