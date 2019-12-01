"""Module to get news on comicsblog.fr."""

import discord
from discord.ext import commands
from utils.tools import get_soup_html


async def get_comicsblog(numb):
    """Get latest news on comicsblog.fr.

    Args:
        numb (int): number of news to retrieve

    Returns:
        list: list of comicsblog news

    """
    num = int(numb)
    c_blog_rss = "http://www.comicsblog.fr/comicsblog.rss"

    soup = await get_soup_html(c_blog_rss)
    ls = soup.select('item')
    out = ls[:num]

    return out


class Comicsblog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comicsblog(self, ctx, num):
        """Send latest comicsblog news.

        Args:
            num (int): number of results to send

        """
        list = await get_comicsblog(num)
        embed = discord.Embed(title=f"les {num} derniers articles de comicsblog",  # noqa:E501
                              color=0xe3951a)
        for l in list:
            embed.add_field(name=l.find('title').text, value=l.find('guid').text,  # noqa:E501
                            inline=False)
        await ctx.send(embed=embed)
