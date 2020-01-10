#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Help cog."""

import discord
from discord.ext import commands, tasks

from utils.constants import (helps, help_team, help_above,
                             left_triangle, right_triangle)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Display available commands."""
        embed = discord.Embed(title="Page 1/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)  # noqa: E501
        embed_2 = discord.Embed(title="Page 2/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)  # noqa: E501
        for s in helps:
            if len(embed.fields) < 10:
                embed.add_field(name=s['name'], value=s['value'], inline=False)
            else:
                embed_2.add_field(name=s['name'], value=s['value'], inline=False)
        if ctx.author.top_role >= self.bot.role_dcteam:
            for h in help_team:
                embed_2.add_field(name=h['name'], value=h['value'], inline=False)
        if ctx.author.top_role >= self.bot.role_modo:
            for h in help_above:
                embed_2.add_field(name=h['name'], value=h['value'], inline=False)
        # if ctx.channel.category_id == dcteam_category_id:
            # embed.add_field(name='nsfw', value="affiche une image nsfw", inline=False)  # noqa: E501
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(left_triangle)
        await msg.add_reaction(right_triangle)

        @tasks.loop(seconds=2)
        async def helperloop():
            def check(reaction, user):
                return (ctx.author == user
                        and str(reaction.emoji) in [right_triangle, left_triangle]
                        and msg.id == reaction.message.id)
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)  # noqa: E501
            if str(reaction.emoji) == left_triangle:
                await msg.edit(embed=embed)
            elif str(reaction.emoji) == right_triangle:
                await msg.edit(embed=embed_2)
            else:
                return None
            await reaction.remove(user)
        await msg.delete(delay=60)
        helperloop.start()
