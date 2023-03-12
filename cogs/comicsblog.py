"""Module to get news on comicsblog.fr."""

import discord
from discord.ext import commands
from utils.tools import get_soup_html


async def get_comicsblog(numb: int):
    """Get latest news on comicsblog.fr.

    Args:
        numb (int): number of news to retrieve

    Returns:
        list: list of comicsblog news

    """
    c_blog_rss = "http://www.comicsblog.fr/comicsblog.rss"

    soup = await get_soup_html(c_blog_rss)
    return soup.select('item')[:numb]


class Comicsblog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def comicsblog(self, ctx, num: int):
        """Send latest comicsblog news.

        Args:
            num (int): number of results to send

        """
        articles = await get_comicsblog(num)
        embed = discord.Embed(title=f"les {num} derniers articles de comicsblog",  # noqa:E501
                              color=0xe3951a)
        for art in articles:
            embed.add_field(name=art.find('title').text,
                            value=art.find('guid').text,
                            inline=False)
        await ctx.send(embed=embed)
