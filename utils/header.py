#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""Download header images."""

import os
import shutil
import time
from PIL import Image

import requests
from urllib.parse import urljoin

from utils.tools import get_soup_html

dctrad_base = "http://www.dctrad.fr"
dctrad_url = "http://www.dctrad.fr/index.php"


def _get_header_img(soup, n):
    """Return list of img url.

    n is 1, 2, 3 or 4 for different headers.
    """
    return soup.select(f'#dog{n+1} > center > span.btn-cover a')


def _download_img(h_list, path):
    """Download list of images.

    n is 1, 2, 3 or 4 for different headers.
    """
    for h in h_list[:9]:
        index = h_list.index(h)
        img_url = urljoin(dctrad_base, h.img['src'])
        response = requests.get(img_url, stream=True)
        _file = os.path.join(path, f"ressources/img{index}.jpg")
        with open(_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    del response


def _make_header(n, path):
    """Create header img.

    n is 1, 2, 3 or 4 for different headers.
    """
    jpg_list = []
    for i in range(9):
        _file = os.path.join(path, f"ressources/img{i}.jpg")
        jpg_list.append(_file)

    images = [Image.open(i) for i in jpg_list]

    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_width = max_width * 3
    max_height = max(heights)
    total_height = max_height * 3

    new_im = Image.new('RGB', (total_width, total_height))

    ims_grid = [images[x:x+3] for x in range(0, len(images), 3)]  # noqa: E226

    _file = os.path.join(path,
                         f'ressources/header{n}-{time.strftime("%Y%m%d-%H%M%S")}.jpg')

    x_offset = 0
    y_offset = 0
    for row in ims_grid:
        for im in row:
            new_im.paste(im, box=(x_offset, y_offset))
            x_offset += max_width
        x_offset = 0
        y_offset += max_height

    new_im.save(_file)

    return _file


def get_header(n, path):
    """Get header.

    n is 1, 2, 3 or 4 for different headers.
    """
    soup = get_soup_html(dctrad_url)
    h_list = _get_header_img(soup, n)
    _download_img(h_list, path)
    file_path = _make_header(n, path)
    return file_path
