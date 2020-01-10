#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import asyncio
import sys
import random

import discord
from discord.ext import commands

import cogs

from utils.constants import greeting_list
from utils.logs import CommandLog
from utils.gif_json import GifJson
from utils.reddit import reddit_nsfw
from utils.secret import token, dcteam_role_id, dcteam_id, modo_role_id

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
             cogs.Getcomics,
             cogs.Gifs,
             cogs.Google,
             cogs.Header,
             cogs.Help,
             cogs.Misc,
             cogs.Notifications,
             cogs.Mod,
             cogs.Team,
             cogs.Urban,
             cogs.Youtube]


@bot.event
async def on_ready():
    """Log in Discord."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.guild = bot.get_guild(dcteam_id)  # se lier au serveur à partir de l'ID
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
    channel_general = discord.utils.get(bot.guild.text_channels, name='general')
    greeting = random.choice(greeting_list)
    await asyncio.sleep(delay=36000)  # bot is rebooted every day at 00:00 so we wait 10 hours after logging in
    await channel_general.send(content=greeting)

# @bot.command()
# @commands.is_nsfw()
# async def nsfw(ctx):
    # TODO : doctring
    # await ctx.send(content=reddit_nsfw())

bot.run(token)
