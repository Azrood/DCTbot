#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Urban dictionnary cog."""

from typing import NamedTuple
from urllib.parse import quote
from utils.tools import get_soup_lxml

import discord
from discord.ext import commands

urban_logo = "https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg"  # noqa: E501


class Result(NamedTuple):
    title: str
    meaning: str
    example: str
    url: str


# Class to make request on Urban Dictionary
class UrbanSearch:
    """Class to search on urban dictionary."""

    urban_url = "https://www.urbandictionary.com/define.php?term={}"

    def __init__(self, user_input: str):
        """Init object with user input, search, and get lxml soup."""
        formated_input = quote(user_input.lower())
        # Make search url: www.urbandictionary.com/define.php?term=distro+hop
        self.search_url = self.urban_url.format(formated_input)
        self.soup = None
        self.definition_soup = None
        self.valid: bool = False

    def _isokay(self):
        """Test if the page is a definition, or is dummy."""
        # Test if I can find the div for :
        # Sorry, we couldn't find XXX
        # If not, search is valid
        self.valid = bool(self.definition_soup)

    async def fetch(self) -> None:
        self.soup = await get_soup_lxml(self.search_url)
        self.definition_soup = self.soup.select_one('div.definition')
        self._isokay()

    def get_top_def(self) -> Result:
        """Parse the HTML soup to find Top Definition title, meaning, example."""  # noqa:E501
        title = self.definition_soup.select_one('h1 > a.word').text
        meaning = self.definition_soup.select_one('div.meaning').text
        if example_raw := self.soup.select_one('div.example'):
            example = example_raw.text
        else:
            example = "No example"
        return Result(title=title, meaning=meaning,
                      example=example, url=self.search_url)


class Urban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def urban(self, ctx, *, query: str):
        """Send definition of user input on Urban Dictionary.

        Args:
            query (str): search on Urban Dictionnary.
        """
        urban = UrbanSearch(query)
        await urban.fetch()
        if urban.valid:
            res = urban.get_top_def()
            embed = discord.Embed(title=f"Definition of {res.title[:100]}",
                                  description=res.meaning[:2048], color=0x00FFFF,
                                  url=res.url)
            embed.add_field(name="Example",
                            value=res.example[:2048], inline=False)
            embed.set_thumbnail(url=urban_logo)
        else:
            embed = discord.Embed(title=f"Definition of {query} doesn't exist")
        await ctx.send(embed=embed)
