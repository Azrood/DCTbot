#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import logging
import sys

import discord
from discord.ext import commands

import cogs

from utils.bot_logging import setup_logging
from utils.logs import CommandLog
from utils.gif_json import GifJson
from utils.secret import token, dcteam_role_id, main_guild_id, modo_role_id

prefix = '!'

if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        print("You are in debug mode.")
        print("Prefix is now '?'")
        prefix = '?'

bot = commands.Bot(command_prefix=prefix, help_command=None,
                   description=None, case_insensitive=True)

my_giflist = GifJson("gifs.json")

cogs_list = [cogs.Admin,
             cogs.BonjourMadame,
             cogs.Cards,
             cogs.Comicsblog,
             cogs.Dealabs,
             cogs.ErrorLogs,
             cogs.Getcomics,
             cogs.Gifs,
             cogs.Google,
             cogs.Greetings,
             cogs.Header,
             cogs.Help,
             cogs.Misc,
             cogs.Notifications,
             cogs.Mod,
             cogs.Team,
             cogs.Urban,
             cogs.Youtube
             ]


@bot.event
async def on_ready():
    """Log in Discord."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.guild = bot.get_guild(main_guild_id)  # se lier au serveur à partir de l'ID
    try:
        bot.role_dcteam = bot.guild.get_role(dcteam_role_id)
        bot.role_modo = bot.guild.get_role(modo_role_id)
    except AttributeError:
        bot.role_dcteam = 0
        bot.role_modo = 0
    bot.prefix = prefix
    bot.nsfw_channel = discord.utils.get(bot.guild.text_channels, name='nsfw')  # noqa:E501
    bot.log = CommandLog("logs.json")
    bot.gifs = my_giflist
    for cog in cogs_list:
        bot.add_cog(cog(bot))


setup_logging()
logger = logging.getLogger(__name__)

logger.info("This is an INFO message on the root logger.")
# logger.warning("This is a WARNING message of the root logger")
# logger.error("This is a ERROR message of the root logger")
# logger.critical("This is a CRITICAL message of the root logger")

try:
    logger.info(f"New bot ran with discord.py version : {discord.__version__}")
    bot.run(token)
except Exception:
    logger.critical(f"bot crashed with discord.py version : {discord.__version__}")
    logger.critical("Unexpected critical error", exc_info=True)
