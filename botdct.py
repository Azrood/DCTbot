#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import argparse
import logging
from pathlib import Path

import discord
from discord.ext import commands

import cogs

from utils.bot_logging import setup_logging
from utils.logs import CommandLog
from utils.gif_json import GifJson
from utils.secret import TOKEN, dcteam_role_id, main_guild_id, modo_role_id

setup_logging(Path(__file__).resolve().parent / 'logging.json')
logger = logging.getLogger(__name__)

PREFIX = '!'

# --debug option
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                    help="change prefix to '?'", action="store_true")
args = parser.parse_args()
if args.debug:
    logger.info("You are in debug mode.")
    logger.info("Prefix is now '?'")
    PREFIX = '?'
# done with parsing options with argparser

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix=PREFIX, help_command=None,
                   description=None, case_insensitive=True,
                   intents=intents)

cogs_list = [cogs.Admin,
             #  cogs.BonjourMadame,
             cogs.Browse,
             cogs.Cards,
             cogs.Comicsblog,
             cogs.Dealabs,
             cogs.Getcomics,
             cogs.Gifs,
             cogs.Google,
             #  cogs.Greetings,
             cogs.Header,
             cogs.Help,
             cogs.Misc,
             cogs.Notifications,
             cogs.Mod,
             #  cogs.RedditBabes,
             cogs.Register,
             cogs.Team,
             cogs.Urban,
             cogs.Youtube]


@bot.event
async def on_ready():
    """Log in Discord."""
    logger.info('Logged in as')
    logger.info(bot.user.name)
    logger.info(bot.user.id)
    logger.info('------')
    bot.guild = bot.get_guild(main_guild_id)  # se lier au serveur à partir de l'ID
    try:
        bot.role_dcteam: discord.Role = bot.guild.get_role(dcteam_role_id)
        bot.role_modo: discord.Role = bot.guild.get_role(modo_role_id)
    except AttributeError:
        bot.role_dcteam = 0
        bot.role_modo = 0
    bot.prefix = PREFIX
    bot.nsfw_channel = discord.utils.get(bot.guild.text_channels, name='nsfw')
    bot.log = CommandLog("logs.json")
    bot.gifs = GifJson("gifs.json")
    for cog in cogs_list:
        await bot.add_cog(cog(bot))
    await bot.tree.sync()


# @bot.event
# async def on_command_error(ctx, error):  # pylint: disable=unused-argument
#     """Handle the CommandNotFound errors."""
#     # !<name> is a valid gif, ignore the CommandNotFound Error
#     # code is reversed, error is raised/logged only if the command is not a gif
#     if (not isinstance(error, commands.CommandNotFound)
#             or error.args[0] not in [f'Command "{name}" is not found'
#                                      for name in bot.gifs.gifs]):
#         raise error

# logger.info("This is an INFO message on the root logger.")
# logger.warning("This is a WARNING message of the root logger")
# logger.error("This is a ERROR message of the root logger")
# logger.critical("This is a CRITICAL message of the root logger")

try:
    logger.info("New bot ran with discord.py version : %s", discord.__version__)
    bot.run(TOKEN)
except Exception:
    logger.critical("bot crashed with discord.py version : %s", discord.__version__)
    logger.critical("Unexpected critical error", exc_info=True)
