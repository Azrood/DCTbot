#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cog to get daily on bonjourmadame picture."""

import logging
from pathlib import Path

import asyncpraw  # pip install asyncpraw
import discord
from discord.ext import commands, tasks

from utils.secret import reddit_client_id, reddit_client_secret, reddit_user_agent  # noqa: E501

logger = logging.getLogger(__name__)


class RedditBabes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.babes.start()  # pylint: disable=no-member

    @tasks.loop(hours=1)  # checks the babes subreddit every hour
    async def babes(self):
        """Send babes from reddit."""
        # allready posted babes list
        logger.info("Entering hourly task.")
        nsfw_channel_history: list = [mess async for mess in discord.utils.get(self.bot.guild.text_channels, name='nsfw').history(limit=200)]  # noqa: E501
        last_bot_messages = [
            message.content
            for message in nsfw_channel_history
            if message.author == self.bot.user
            ]
        logger.info("Messages fetched.")
        # Reddit client
        reddit = asyncpraw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent)

        logger.info("Reddit ok.")

        # List of subreddits
        try:
            p = Path(__file__).parent / "redditbabes.txt"
            with open(p, mode='r', encoding='utf-8') as f:
                subreddits = f.read().splitlines()
        except FileNotFoundError:
            logger.error("cogs/redditbabes.txt is missing")
            subreddits = []

        # Iterate on our subreddits
        for sub in subreddits:
            subreddit = await reddit.subreddit(sub, fetch=True)
            logger.info("fetching %s", sub)
            # Iterate on each submission
            async for submission in subreddit.hot(limit=10):
                if submission.stickied:
                    continue
                url = submission.url
                if url not in last_bot_messages:
                    # TODO: I let some codes, if we want to change, with only sends
                    # or with a full embed (with the set_image thing)
                    # we can decide later.
                    # await self.bot.nsfw_channel.send(submission.title)
                    # await self.bot.nsfw_channel.send(url)
                    embed = discord.Embed(title=submission.title,
                                          url=f"https://www.reddit.com{submission.permalink}",
                                          )
                    # embed.set_image(url=url)
                    await self.bot.nsfw_channel.send(embed=embed)
                    await self.bot.nsfw_channel.send(url)
        await reddit.close()
        logger.info("Exiting hourly task.")

    @babes.before_loop
    async def before_babes(self):
        """Intiliaze babes loop."""
        await self.bot.wait_until_ready()
