#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Cards cog."""

from pathlib import Path

import discord
from discord.ext import commands


class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards_dir = Path(__file__).resolve().parents[1] / "pictures" / "cards"
        self.cards_list = [child.stem for child in self.cards_dir.iterdir()]

    @commands.hybrid_command()
    async def poke(self, ctx, people: str):
        """Send card made by Slyrax."""
        people = people.lower()
        if people == "help":  # probably needs improvements
            embed = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>",
                                  description="\n".join(self.cards_list))
            embed.set_footer(text="Merci à Slyrax pour les cartes !")
            await ctx.send(embed=embed)

        elif people in self.cards_list:
            card_file = self.cards_dir / f"{people}.jpg"  # noqa: E501
            f = discord.File(fp=card_file, filename=f"{people}.jpg")
            await ctx.send(file=f)
