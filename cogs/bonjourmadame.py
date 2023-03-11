#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cog to get daily on bonjourmadame picture."""

import datetime
# from pytz import timezone
import logging
from pathlib import Path

from discord.ext import commands, tasks

from utils.tools import get_soup_html

logger = logging.getLogger(__name__)


async def latest_madame():
    """Fetch last Bonjourmadame picture."""
    url = "https://www.bonjourmadame.fr/"
    soup = await get_soup_html(url)

    # Title and content
    content = soup.select_one("div.post-content > p")
    title = soup.select_one("header.post-header > h1 > a")

    title_txt, book, image_url = None, None, None
    if title:  # TITLE
        title_txt = title.text
    if a := content.find('a', href=True):  # book is the link to the private book of the model
        book: str = a['href']
    if image := content.find('img', src=True):  # image URL
        image_url: str = image['src'].split('?')[0]
    return image_url, title_txt, book


class BonjourMadame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bonjour_madame.start()  # pylint: disable=no-member

    # @tasks.loop(hours=24)
    @tasks.loop(time=datetime.time(hour=9, minute=30))  # THIS WORKS, but with an offset (9h30 actually triggers at 10h30 in winter)
    async def bonjour_madame(self):
        """Send daily bonjourmadame."""
        if not 0 <= datetime.date.today().weekday() <= 4:
            return
        url, title, book = await latest_madame()
        logger.info("try to post madame with %s / %s / %s", url, title, book)
        if url:
            await self.bot.nsfw_channel.send(title)
            await self.bot.nsfw_channel.send(url)
            logger.info("madame sent")
        if book:
            try:
                p = Path(__file__).parent / "bonjour_exclude.txt"
                with open(p, mode='r', encoding='utf-8') as f:
                    excludes = f.read().splitlines()
            except FileNotFoundError:
                logger.error("cogs/bonjour_excludes.txt is missing")
                excludes = []
            if any(excl in book for excl in excludes):
                logger.info("bonjourmadame book was found, but excluded")
            else:
                await self.bot.nsfw_channel.send(book)
                logger.info("madame had a book, sent.")

    @bonjour_madame.before_loop
    async def before_bonjour_madame(self):
        """Intiliaze bonjour_madame loop."""
        await self.bot.wait_until_ready()
        # await asyncio.sleep(41400)  # Wait 10hours 30min, to lauch at 10:30AM
