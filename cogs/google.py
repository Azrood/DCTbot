# -*- coding: utf-8 -*-
"""Google cog."""


# import os
import aiohttp
import contextlib
import json
from urllib.parse import quote_plus
from typing import NamedTuple, List, Dict

import discord
from discord.ext import commands

from utils.secret import TOKEN_YOUTUBE, DEVELOPER_CX


class Result(NamedTuple):
    title: str
    url: str


async def search_google(user_input: str, number: int) -> List[Result]:
    """Search on Google.

    Args:
        user_input (str): users's search on Google
        number (int): number of responses

    Returns:
        list: list of results (list of namedtuple with 'title' and 'link' keys)

    """
    google_search_url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'q': quote_plus(user_input),
        'cx': DEVELOPER_CX,
        'safe': 'active',
        'hl': 'fr',
        'num': number,
        'fields': 'items(kind,link,title)',
        'key': TOKEN_YOUTUBE,
    }
    session = aiohttp.ClientSession()

    response = await session.get(google_search_url,
                                 params=params, timeout=3, ssl=False)
    text = await response.text()
    await session.close()

    try:
        json_data: List[Dict] = json.loads(text)["items"]
    except KeyError:  # pragma: no cover
        json_data = []

    return [Result(j['title'], j['link']) for j in json_data]


async def google_top_link(user_input: str) -> Result:
    """Get first result of Google search.

    Args:
        user_input (str): users's search on Google

    Returns:
        dict: dict with keys 'title' and 'link'

    """
    try:
        results = await search_google(user_input, number=1)
        return results[0]
    except IndexError:  # pragma: no cover
        return None


class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def google(self, ctx: commands.Context, *, query: str):
        """Send first Google search result.

        Args:
            query (str): Search on google.
        """
        with contextlib.suppress(TypeError):
            result = await google_top_link(query)
            await ctx.send(content=f"{result.title}\n{result.url}")

    @commands.hybrid_command()
    async def googlelist(self, ctx, num: int, *, args: str):
        """Send Google search results.

        Args:
            num (int): number of results desired.
            args (str): Search on google.
        """
        results = await search_google(args, num)
        embed = discord.Embed(title=f"Les {num} premiers résultats de la recherche",  # noqa: E501
                              color=0x3b5cbe)
        for res in results:
            embed.add_field(name=res.title, value=res.url, inline=False)
        await ctx.send(embed=embed)
