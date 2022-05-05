#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""


import asyncio
import logging
import random

import discord
from discord.ext import commands

dctradlogo = "http://www.dctrad.fr/ext/planetstyles/flightdeck/store/logodctweb.png"  # noqa: E501
dctrad_recru = "http://www.dctrad.fr/viewforum.php?f=21"
snap_url = "https://media.tenor.com/images/8d7d2e757f934793bb4154cede8a4afa/tenor.gif"  # noqa: E501

logger = logging.getLogger(__name__)


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recrutement(self, ctx):
        """Send 'recrutement' topic url."""
        embed = discord.Embed(title="Rejoins la team DCTrad !",
                            description="allez n'aie pas peur de cliquer et deviens un héros !",  # noqa: E501
                            color=0x0000FF, url=dctrad_recru)
        embed.set_thumbnail(url=dctradlogo)
        await ctx.send(embed=embed)

    @commands.command()
    async def timer(self, ctx, numb, *, args):
        """Program a timer."""
        num = int(numb)
        await ctx.send(content=f"{ctx.author.mention} : timer enregistré !",
                       delete_after=10)
        await asyncio.sleep(num, result=None, loop=None)
        await ctx.send(content=f"temps écoulé ! : {ctx.author.mention} {args}")

    @commands.command()
    async def choose(self, ctx, *choices):
        """Randomly choose user's choices."""
        if len(choices) < 1:  # pragma: no cover
            return None
        await ctx.send(random.choice(choices))

    @commands.command()
    async def coinflip(self, ctx):
        """Launch a coinflip and print 'pile' or 'face'."""
        await ctx.send(random.choice(["pile", "face"]))

    @commands.command()
    async def say(self, ctx, *, args):
        """Bot writes user message content, and delete original user message."""  # noqa:E501
        await ctx.message.delete()
        await ctx.send(content=args)

    @commands.command()
    async def edit(self, ctx, id, *, args):
        """Bot can edit is own message."""
        msg = await ctx.fetch_message(id)
        await msg.edit(content=args)
        await ctx.message.delete()

    @commands.command()
    async def ping(self, ctx):
        """Ping the bot."""
        await ctx.send(content="pong !")
        logger.info(f"Ping (asked by {ctx.author}) was awaited.")

    @commands.command()
    async def roulette(self, ctx):
        """Plays russian roulette and kick user if shot."""
        if random.randrange(6) == 3:
            await ctx.send(content=random.choice(["Pan !",
                                                  "I am inevitable !",
                                                  "Say my name",
                                                  "Bye bitch !",
                                                  "Omae wa mou shindeiru",
                                                  "Boom",
                                                  "Hasta la vista baby !"
                                                  "Ca va péter !",
                                                  "Il va faire nuit !"]))

            await ctx.send(content=snap_url, delete_after=4)
            await asyncio.sleep(2.4, result=None, loop=None)
            await ctx.author.kick()
        else:
            close = random.choice([
                "*clic*....Tu restes vivant !",
                "Ouh c'était chaud !",
                f"Dios mio that was close sinior {ctx.author.mention}",
                "T'as toujours toute ta tête mon petit gars ?",
                "J'en connais qui a vu la mort en face !",
                "Ouh à un cheveu près ! Allez la prochaine c'est la bonne !",
                "MAIS T'ES MALADE !",
                "C'est bientot fini ?"
                ])
            await ctx.send(content=close)
