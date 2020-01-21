#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Getcomics cog."""

import discord
from discord.ext import commands

import asyncio
import aiohttp  # lib for going on internet
import urllib.parse
from utils.tools import get_soup_html


async def getcomics_top_link(user_input):
    """Search getcomics and return first result."""
    formated_search = urllib.parse.quote_plus(user_input.lower(),
                                              safe='', encoding=None,
                                              errors=None)
    getcomics_search = f"https://getcomics.info/?s={formated_search}"

    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = await get_soup_html(getcomics_search)

    first = soup.select_one('article')  # The whole first post (with cover, title, synopsis, etc...)  # noqa: E501
    cover = first.select_one("div.post-header-image > a > img")["src"].split('?')[0]  # noqa: E501
    link = first.select_one("h1 > a")
    title = link.text
    url = link["href"]
    url_dl = await getcomics_directlink(url)
    return title, url_dl, cover


async def getcomics_directlink(comic_url):
    """Get download links in a getcomics post."""
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = await get_soup_html(comic_url)

    direct_download = soup.find('a', class_='aio-red')

    # temp_url is not the final cbz or cbr download url
    temp_url = direct_download['href']

    # We follow temp_url to find final URL
    await asyncio.sleep(1)

    session = aiohttp.ClientSession()

    res2 = await session.get(temp_url, allow_redirects=False, timeout=3, ssl=False)  # noqa:E501
    await session.close()

    if res2.status == 200:
        # print("req 2 code 200")
        return res2.url
    elif res2.status == 302:
        # print("302, Found Comic URL")
        return res2.headers['location']
    elif res2.status == 404:
        # print('404, returning post url')
        # in this case, return the getcomics post url
        return comic_url
    else:
        # in this case, return the getcomics post url
        # print("unkwnown response code")
        return comic_url


class Getcomics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def getcomics(self, ctx, *, user_input):
        """Send direct download link for getcomics search result."""
        title, url, cover = await getcomics_top_link(user_input)
        embed = discord.Embed(title=f"{title}",
                            description="cliquez sur le titre pour télécharger votre comic",  # noqa: E501
                            color=0x882640, url=url)
        embed.set_image(url=cover)
        await ctx.send(embed=embed)
