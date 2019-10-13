#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""Download header images."""

import os
import shutil
import time
from PIL import Image

import numpy as np
import requests
from urllib.parse import urljoin

from utils.tools import get_soup_html

dctrad_base = "http://www.dctrad.fr"
dctrad_url = "http://www.dctrad.fr/index.php"


def _get_header_img(soup, n):
    """Return list of img url.

    n is 1, 2,  or 4 for different headers.
    """
    return soup.select(f'#dog{n+1} > center > span.btn-cover a')


def _download_img(h_list, path):
    """Download list of images.

    n is 1, 2,  or 4 for different headers.
    """
    for h in h_list[:9]:
        index = h_list.index(h)
        img_url = urljoin(dctrad_base, h.img['src'])
        response = requests.get(img_url, stream=True)
        _file = os.path.join(path, f"ressources/img{index}.png")
        with open(_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    del response


def _make_header(n, path):
    """Create header img.

    n is 1, 2,  or 4 for different headers.
    """
    # Code found on Stackoverflow.
    # It just works.
    png_list = []
    for i in range(9):
        _file = os.path.join(path, f"ressources/img{i}.png")
        png_list.append(_file)

    imgs = [Image.open(i) for i in png_list]

    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted([(sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack([i.resize(min_shape) for i in imgs])

    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    # Add a time stamp to the file name, so that Discord can't use cache
    _file = os.path.join(path,
                         f'ressources/header{n}-{time.strftime("%Y%m%d-%H%M%S")}.jpg')
    imgs_comb.save(_file)
    return _file


def get_header(n, path):
    """Get header.

    n is 1, 2,  or 4 for different headers.
    """
    soup = get_soup_html(dctrad_url)
    h_list = _get_header_img(soup, n)
    _download_img(h_list, path)
    file_path = _make_header(n, path)
    return file_path
