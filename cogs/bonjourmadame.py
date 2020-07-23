#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cog to get daily on bonjourmadame picture."""

import asyncio
import datetime

import discord
from discord.ext import commands, tasks

from utils.tools import get_soup_lxml


async def latest_madame():
    """Fetch last Bonjourmadame picture."""
    madames = "http://feeds2.feedburner.com/BonjourMadame"
    soup = await get_soup_lxml(madames)
    item = soup.find('item')

    try:
        url = item.find('img')['src']
        return url.split('?')[0]
    except TypeError as e:
        print(e, "Madame is not an image")

    try:
        url = item.find("video").find("source")['src']
        return url.split('?')[0]
    except TypeError as e:  # pragma: no cover
        print(e, "Madame is not a video")
        return None


class BonjourMadame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bonjour_madame.start()  # pylint: disable=no-member

    # time=date.time(hour=10)  will use it when it is released :D
    @tasks.loop(hours=24)  # will take time as argument when v1.3 is released  # noqa: E501
    async def bonjour_madame(self):
        """Send daily bonjourmadame."""
        if 0 <= datetime.date.today().weekday() <= 4:  # check the current day, days are given as numbers where Monday=0 and Sunday=6  # noqa: E501
            url = await latest_madame()
            if url:
                await self.bot.nsfw_channel.send(url)

    @bonjour_madame.before_loop
    async def before_bonjour_madame(self):
        """Intiliaze bonjour_madame loop."""
        await self.bot.wait_until_ready()
        await asyncio.sleep(37800)  # Wait 10hours 30min, to lauch at 10:30AM
