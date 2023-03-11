"""Module to get the free games from Dealabs"""

import logging
from typing import List, NamedTuple

from utils.tools import get_soup_xml

import discord
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


class Game(NamedTuple):
    title: str
    url: str


async def get_free_games() -> List[Game]:
    """returns list of named tuple of free games from Dealabs.
        `[(title,url),(title,url)]`
    """
    free_games = "https://www.dealabs.com/rss/groupe/gratuit"
    items = (await get_soup_xml(free_games)).select('item')

    # take everything from the rss feed
    res = [i.find_all(['category', 'title', 'link']) for i in items]

    # construct a list of tuple [(title,url)] with games from the result set
    try:
        games_list = [Game(title=r[1].text, url=f"<{r[2].text}>")  # the < > are for preventing the embed in discord
                      for r in res if "jeu" in r[0].text.lower()]
        return games_list
    except IndexError:
        return []


class Dealabs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.auto_free_games.start()  # pylint: disable=no-member

    @tasks.loop(hours=1)  # checks the dealabs feed every hour
    async def auto_free_games(self):
        """"Sends links of free games from Dealabs"""
        free_game_list = await get_free_games()
        free_game_channel_history: List[discord.Message] = [message async for message in discord.utils.get(self.bot.guild.text_channels, name="jeux-video-gratuits").history(limit=50)]  # noqa: E501
        free_game_role = discord.utils.get(
            self.bot.guild.roles,
            name="jeux gratuits"
            )
        # get games posted by bot in the free games channel
        last_posted_free_games = [message.content
                                  for message in free_game_channel_history
                                  if message.author == self.bot.user]

        # filter the free game list retrieved by dealabs from games already posted
        games_not_posted = ["\n".join(game) + "\n"
                            for game in free_game_list
                            if game.title not in "".join(last_posted_free_games)]

        if games_not_posted:
            await discord.utils.get(
                self.bot.guild.text_channels,
                name="jeux-video-gratuits"
                ).send(content=f"{free_game_role.mention} {' '.join(games_not_posted)}")
            logger.info("Posted games")
        else:
            logger.info("No new games")

    @auto_free_games.before_loop
    async def before_free_games(self):
        """Intiliaze free_games loop."""
        await self.bot.wait_until_ready()
