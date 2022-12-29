#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""Download header images."""

import os
import shutil
import time
import datetime
from PIL import Image
import io  # will use it to convert the bytes read with aiohttp to file-like object  # noqa:E501
import aiohttp
from urllib.parse import urljoin

import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from utils.tools import get_soup_html

dctrad_base = "https://www.dctrad.fr"
dctrad_url = f"{dctrad_base}/index.php"


def _get_header_img(soup, n: int):
    """Return list of img url.

    n is 1, 2, 3 or 4 for different headers.
    """
    res = soup.select(f'#dog{n+1} > div > span.btn-cover img')
    return res


async def _download_img(h_list: list, path: os.PathLike):
    """Download list of images.

    n is 1, 2, 3 or 4 for different headers.
    """
    session = aiohttp.ClientSession()
    for h in h_list[:9]:
        index = h_list.index(h)
        img_url = urljoin(dctrad_base, h['src'])
        resp = await session.get(url=img_url)
        buffer = io.BytesIO(await resp.read())  # buffer is a file-like object
        file_ = os.path.join(path, f"img{index}.jpg")
        with open(file_, 'wb') as out_file:
            shutil.copyfileobj(buffer, out_file)
    await session.close()


def _make_header(n: int, path: os.PathLike) -> str:
    """Create header img.

    n is 1, 2, 3 or 4 for different headers.
    """
    jpg_list = [os.path.join(path, f"img{i}.jpg") for i in range(9)]

    images = [Image.open(i) for i in jpg_list]

    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_width = max_width * 3
    max_height = max(heights)
    total_height = max_height * 3

    new_im = Image.new('RGB', (total_width, total_height))

    file_ = os.path.join(path, f'header{n}-{time.strftime("%Y%m%d-%H%M%S")}.jpg')  # noqa: E501

    for index, image in enumerate(images):
        i, j = divmod(index, 3)
        x_offset = j * max_width
        y_offset = i * max_height
        new_im.paste(image, box=(x_offset, y_offset))

    new_im.save(file_)

    # clean - delete the covers
    for jpg in jpg_list:
        os.remove(jpg)

    return file_


async def get_monthly_url() -> str:
    """Get 'Comics du mois' topic url."""
    year = datetime.date.today().year
    month = datetime.date.today().month
    monthly_url = f"{dctrad_base}/app.php/releases/{year}/{month}"
    return monthly_url


async def get_header(n: int) -> str:

    """Get header.

    n is 1, 2, 3 or 4 for different headers.
    """
    # Compute path (ie : ./../ressoures/)
    dirname = os.path.dirname(__file__)  # -> ./
    ress_path = os.path.join(dirname, os.pardir, "ressources")  # -> ./../ressources  # noqa:E501

    soup = await get_soup_html(dctrad_url)
    h_list = _get_header_img(soup, n)
    await _download_img(h_list, ress_path)
    file_path = _make_header(n, ress_path)
    return file_path


class Header(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def header(self, ctx, arg: str):
        """Send header image."""
        arg = arg.lower()
        monthly = await get_monthly_url()
        embed = discord.Embed(title="Comics du mois", url=monthly)
        if arg == "rebirth" or arg == "dcrebirth":
            file_path = await get_header(1)
            await ctx.send(embed=embed, file=discord.File(file_path))
        elif arg == "hors" or arg == "horsrebirth":
            file_path = await get_header(2)
            await ctx.send(embed=embed, file=discord.File(file_path))
        elif arg in ["indé", "indés", "inde", "indé"]:
            file_path = await get_header(3)
            await ctx.send(embed=embed, file=discord.File(file_path))
        elif arg == "marvel":
            file_path = await get_header(4)
            await ctx.send(embed=embed, file=discord.File(file_path))
        try:
            os.remove(file_path)
        except OSError:
            pass

    # TODO : it seems we can't make a hybrid command, with the slash-command havint the  choice
    @app_commands.command()
    @app_commands.describe(editor='Choose an editor')
    @app_commands.choices(editor=[
        Choice(name='DC Rebirth', value=1),
        Choice(name='DC Hors Rebirth', value=2),
        Choice(name='Indé / Vertigo', value=3),
        Choice(name='Marvel', value=4),
    ])
    async def headerdct(self, interaction: discord.Interaction, editor: Choice[int]):
        monthly = await get_monthly_url()
        embed = discord.Embed(title="Comics du mois", url=monthly)
        file_path = await get_header(editor.value)
        await interaction.response.send_message(embed=embed, file=discord.File(file_path))
        try:
            os.remove(file_path)
        except OSError:
            pass
