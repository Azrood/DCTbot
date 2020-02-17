#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Gifs cog."""

import discord
from discord.ext import commands

from utils.secret import dcteam_category_id


class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, ctx, name):
        """Send gif corresponding to 'name'."""
        name = name.lower()

        if name == 'help':

            try:  # if in team category
                if ctx.channel.category_id == dcteam_category_id:
                    list_names = self.bot.gifs.get_names_string(private=False)
                else:
                    list_names = self.bot.gifs.get_names_string(private=True)
            except AttributeError:  # pragma: no cover
                list_names = self.bot.gifs.get_names_string(private=True)
                # channel.category_id will fail in DM messages
                # DMChannel' object has no attribute 'category_id

            embed = discord.Embed(title="liste des gifs",
                                  description=list_names, color=0x000FF)
            await ctx.send(embed=embed)

        if self.bot.gifs.get_gif(name) is not None:
            embed = discord.Embed()
            try:
                if (self.bot.gifs.get_gif(name)['public']
                        or ctx.channel.category_id == dcteam_category_id):
                    gif_url = self.bot.gifs.get_gif(name)['url']
                    embed.set_image(url=gif_url)
                    await ctx.send(embed=embed)
            except AttributeError:  # pragma: no cover
                # channel.category_id will fail in DM messages
                # DMChannel' object has no attribute 'category_id
                if self.bot.gifs.get_gif(name)['public']:
                    gif_url = self.bot.gifs.get_gif(name)['url']
                    embed.set_image(url=gif_url)
                    await ctx.send(embed=embed)
        else:
            pass

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """Read all message and check if it's a gif command."""
        channel = ctx.channel
        # Find if custom command exist in dictionary
        embed = discord.Embed()
        for key in self.bot.gifs.gifs.keys():
            # Added simple hardcoded prefix
            command = self.bot.prefix + key
            if ctx.content.lower() == command:
                try:
                    if (self.bot.gifs.get_gif(key)['public']
                            or ctx.channel.category_id == dcteam_category_id):
                        gif_url = self.bot.gifs.get_gif(key)['url']
                        embed.set_image(url=gif_url)
                        await channel.send(embed=embed)
                except AttributeError:  # pragma: no cover
                    # channel.category_id will fail in DM messages
                    # DMChannel' object has no attribute 'category_id
                    if self.bot.gifs.get_gif(key)['public']:
                        gif_url = self.bot.gifs.get_gif(key)['url']
                        embed.set_image(url=gif_url)
                        await channel.send(embed=embed)
