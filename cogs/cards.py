#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cards cog."""

import os

import discord
from discord.ext import commands


class Cards(commands.Cog):
    def __init__(self, bot):
        self.help = "azrod\nbane\nrun\nsergei\nxanatos\nphoe"
        self.bot = bot

    @commands.command()
    async def poke(self, ctx, people):
        """Send card made by Slyrax."""
        people = people.lower()
        if people == "help":  # probably needs improvements
            embed = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>", description=self.help)  # use this to get by until improvement  # noqa: E501
            embed.set_footer(text="Merci à Slyrax pour les cartes !")
            await ctx.send(embed=embed)

        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            card_file = os.path.join(dir_path, os.pardir, f"pictures/cards/{people}.jpg")  # noqa: E501
            f = discord.File(fp=card_file, filename=people+".jpg")  # discord.File can't handle f-strings apparently  # noqa: E501,E226
            embed = discord.Embed()
            embed.set_image(url="attachment://"+people+".jpg")  # better safe than sorry  # noqa: E501,E226
            await ctx.send(file=f, embed=embed)
