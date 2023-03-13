#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Register cog."""

import asyncio
import logging
from string import ascii_uppercase
from urllib.parse import urljoin

import aiohttp
import discord
from discord.ext import commands
from pyphpbb_sl import PhpBB

from cogs.forum.parseforum import get_all_topics, get_nb_topics, get_sub_forums
from utils.secret import forum_host, forum_password, forum_user_name

logger = logging.getLogger(__name__)


def make_letters_list(input_list, start_index: int = 0):
    out = []
    if input_list:
        out.extend(f"{ascii_uppercase[i]:.<5s}{res['name']}"
                   for i, res in enumerate(input_list, start_index))
    return out


def make_numbers_list(input_list, start_index=0):
    out = []
    if input_list:
        out.extend(
            f"{i:.<5d}{res['name']}"
            for i, res in enumerate(input_list, start_index)
        )
    return out


def make_embed1(sub_forums, topics, active_topics_flag, topics_page):
    embed = discord.Embed()
    if sub_forums:
        forums_value = "\n".join(make_letters_list(sub_forums))
        embed.add_field(name='Forums', value=forums_value, inline=False)
    if topics and not active_topics_flag:
        topics_value = "\n".join(make_numbers_list(topics[topics_page * 10:(topics_page + 1) * 10],  # noqa: E226
                                                   start_index=1))
        embed.add_field(name='Topics', value=topics_value, inline=False)
    return embed


def make_embed2(nb_topics):
    if nb_topics > 10:
        choices = ("- une lettre/un nombre pour naviguer\n"
                   "- 'ù' pour remonter dans le dossier précédent\n"
                   "- '!' pour la prochaine page de topics (10 suivants)\n"
                   "- ':' pour la page précédente de topics (10 d'avant)\n"
                   "- 'exit' pour sortir.\n")
    else:
        choices = ("- un nombre pour naviguer dans un dossier\n"
                   "- 'ù' pour remonter dans le dossier précédent\n"
                   "- 'exit' pour sortir.\n")
    embed2 = discord.Embed(title="Entrez un choix :",
                           description=choices)
    return embed2


class Browse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def browse(self, ctx):
        """Browse de forum.
        """
        phpbb = PhpBB(forum_host)
        async with ctx.channel.typing():
            is_logged = await phpbb.login(forum_user_name, forum_password)
        if not is_logged:
            logger.error("Not logged in forum.")
            return
        current_url = "viewforum.php?f=11"
        last_url = []
        topics_page = 0
        nb_topics = 0
        while True:  # Infinite loop for user inputs
            url = urljoin(forum_host, current_url)
            try:
                async with ctx.channel.typing():
                    html = await phpbb.browser.get_html(url)
            except aiohttp.client_exceptions.ServerDisconnectedError:
                continue
            # List forums and topics, and send them in embed
            sub_forums = get_sub_forums(html)
            active_topics_flag = html.find(id="active_topics", string="Sujets actifs")
            topics = await get_all_topics(phpbb, html, url)
            nb_topics = get_nb_topics(html)

            embed1 = make_embed1(sub_forums, topics, active_topics_flag, topics_page)
            send1 = await ctx.send(embed=embed1)

            embed2 = make_embed2(nb_topics)
            send2 = await ctx.send(embed=embed2)

            def check(message):
                cont = message.content
                return (message.author == ctx.author
                        and (cont.isalnum() and len(cont) == 1
                             or cont in ["exit", "!", ":"]))

            # Wait for response and process.
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=20)
                choice = msg.content

                # TODO : uncomment
                # await ctx.message.delete(delay=None)
                await msg.delete(delay=1)
                await send1.delete(delay=1)
                await send2.delete(delay=1)

                if choice == "exit":
                    break

                # Nested loop for navigate between topics of sub-forum without
                # havint to reparse it. (topics already contain all topics.)
                while choice in ['!', ':']:
                    if choice == '!' and topics_page < nb_topics // 10:
                        topics_page += 1
                    if choice == ':' and topics_page > 0:
                        topics_page -= 1
                    embed3 = make_embed1(None, topics, active_topics_flag, topics_page)
                    send3 = await ctx.send(embed=embed3)
                    embed4 = make_embed2(nb_topics)
                    send4 = await ctx.send(embed=embed4)
                    msg = await self.bot.wait_for("message", check=check, timeout=20)
                    choice = msg.content
                    # TODO
                    await msg.delete(delay=1)
                    await send3.delete(delay=1)
                    await send4.delete(delay=1)

                if choice.isdigit():
                    choice = int(choice)
                    t = topics[topics_page * 10 + choice - 1]  # noqa: E226
                    url = urljoin(forum_host, t['url'])
                    embed5 = discord.Embed(title=f"{t['name']}",
                                           color=0x882640,
                                           url=url)
                    await ctx.send(embed=embed5)
                    break

                # current_url is actually defined here for the NEXT iteration
                if choice == "ù":
                    try:
                        current_url = last_url.pop()
                    except IndexError:
                        current_url = "viewforum.php?f=11"
                else:
                    last_url.append(current_url)
                    current_url = sub_forums[ascii_uppercase.index(choice.upper())].get('url')

            except asyncio.TimeoutError:
                await ctx.send("Tu as pris trop de temps pour répondre !",
                               delete_after=5)
                break

        await phpbb.logout()
        await phpbb.close()

    async def cog_command_error(self, ctx, error):
        logger.error(error, exc_info=True)
        # await ctx.send(error)
