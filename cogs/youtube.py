# -*- coding: utf-8 -*-
"""Youtube cog."""

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import asyncio
# import os
import html

import discord
from discord.ext import commands
import googleapiclient.discovery

from utils.secret import token_youtube
from utils.tools import string_is_int


def search_youtube(user_input, number):
    """Search on Youtube.

    Args:
        user_input (str): search string
        number (int): number of search results

    Returns:
        list: list of results

    """
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = token_youtube

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(  # pylint: disable=no-member
        part="snippet",
        maxResults=number,
        q=user_input
    )
    response = request.execute()

    list = response["items"]

    out = []

    for l in list:
        title = html.unescape(l['snippet']['title'])
        try:
            if l['id']['kind'] == "youtube#channel":
                type = 'channel'
                id = l['id']['channelId']
            elif l['id']['kind'] == "youtube#playlist":
                type = 'playlist'
                id = l['id']['playlistId']
            elif l['id']['kind'] == "youtube#video":
                type = 'video'
                id = l['id']['videoId']
            else:
                type = 'unknown'
                id = "NoID"
        except KeyError:
            type = 'unknown'
            id = "NoID"

        out.append({'title': title, 'type': type, 'id': id})

    return out


def youtube_top_link(user_input):
    """Return title and url of 1st Youtube search.

    Args:
        user_input (str): user search on Youtube

    Returns:
        tuple: title, url

    """
    result = search_youtube(user_input, number=1)
    try:
        url = get_youtube_url(result[0])
        return result[0]['title'], url
    except IndexError:
        pass


def get_youtube_url(result):
    """Make youtube url of 'result' (video, playlist, or channel)."""
    if result['type'] == 'video':
        url = f"https://www.youtube.com/watch?v={result['id']}"
    elif result['type'] == 'playlist':
        url = f"https://www.youtube.com/playlist?list={result['id']}"
    elif result['type'] == 'channel':
        url = f"https://www.youtube.com/channel/{result['id']}"
    else:
        url = None
    return url


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def youtube(self, ctx, *, user_input):
        """Send first Youtube search result."""
        title, url = youtube_top_link(user_input.lower())
        link = await ctx.send(content=f"{title}\n{url}")

        def check(message):
            return message == ctx.message
        await self.bot.wait_for("message_delete", check=check, timeout=1200)
        await link.delete(delay=None)

    @commands.command()
    async def youtubelist(self, ctx, num, *, query):
        """Send n Youtube search results."""
        number = int(num)
        if number > 10:
            number = 10
        result = search_youtube(user_input=query, number=number)
        embed = discord.Embed(color=0xFF0000)
        embed.set_footer(text="Tapez un nombre pour faire votre choix "
                              "ou dites \"cancel\" pour annuler")
        for s in result:
            url = get_youtube_url(s)
            embed.add_field(name=f"{result.index(s)+1}.{s['type']}",
                            value=f"[{s['title']}]({url})", inline=False)
        self_message = await ctx.send(embed=embed)

        def check(message):
            return (message.author == ctx.author
                    and (message.content == "cancel"
                         or string_is_int(message.content)))
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=15)
            if msg.content == "cancel":
                await ctx.send("Annulé !", delete_after=5)
                await self_message.delete(delay=None)
                await ctx.message.delete(delay=2)
                await msg.delete(delay=1)
            else:
                num = int(msg.content)
                if 0 < num <= len(result):
                    url = get_youtube_url(result[num - 1])
                    await ctx.send(content=f"{url}")
                    await ctx.message.delete(delay=2)
                    await self_message.delete(delay=None)
                    await msg.delete(delay=1)

        except asyncio.TimeoutError:
            await ctx.send("Tu as pris trop de temps pour répondre !",
                           delete_after=5)
            await self_message.delete(delay=None)
            await ctx.message.delete(delay=2)
