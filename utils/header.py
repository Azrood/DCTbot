#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""Download header images."""

import os
import shutil
import time
from PIL import Image
import io # will use it to convert the bytes read with aiohttp to file-like object
import aiohttp
from urllib.parse import urljoin

from utils.tools import get_soup_html, get_soup_lxml

dctrad_base = "http://www.dctrad.fr"
dctrad_url = "http://www.dctrad.fr/index.php"


def _get_header_img(soup, n):
    """Return list of img url.

    n is 1, 2, 3 or 4 for different headers.
    """
    return soup.select(f'#dog{n+1} > center > span.btn-cover a')


async def _download_img(h_list, path):
    """Download list of images.

    n is 1, 2, 3 or 4 for different headers.
    """
    session = aiohttp.ClientSession()
    for h in h_list[:9]:
        index = h_list.index(h)
        img_url = urljoin(dctrad_base, h.img['src'])
        resp = await session.get(url=img_url) 
        buffer = io.BytesIO(await resp.read()) # buffer is a file-like object
        file_ = os.path.join(path, f"img{index}.jpg")
        with open(file_, 'wb') as out_file:
            shutil.copyfileobj(buffer, out_file)
    await session.close()
    del resp


def _make_header(n, path):
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

    return file_


async def get_monthly_url():
    """Get 'Comics du mois' topic url."""
    # TODO
    # Class ?
    # For not fetching soup again ?
    soup = await get_soup_lxml(dctrad_url)
    monthly_url = soup.select_one(
        'div#dog2 > center > span.text > a.btn-cm')['href']
    # #dog2 > center > span.text > a.btn-cm
    return monthly_url


async def get_header(n):

    """Get header.

    n is 1, 2, 3 or 4 for different headers.
    """
    # Compute path (ie : ./../ressoures/)
    dirname = os.path.dirname(__file__)  # -> ./
    ress_path = os.path.join(dirname, os.pardir, "ressources/")  # -> ./../ressources  # noqa:E501

    soup = await get_soup_html(dctrad_url)
    h_list = _get_header_img(soup, n)
    await _download_img(h_list, ress_path)
    file_path = _make_header(n, ress_path)
    return file_path
