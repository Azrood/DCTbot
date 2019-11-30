#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""


import unittest

from cogs.getcomics import getcomics_top_link
from cogs.google import google_top_link
from cogs.urban import UrbanSearch
from cogs.youtube import youtube_top_link

from utils.comicsblog import get_comicsblog
from utils.gif_json import GifJson


class TestDiscordBot(unittest.TestCase):
    """Run unit tests."""

    # Each method with name beginning with 'test_'
    # is a test.

    async def test_google_top_link(self):
        """Test google_top_link."""
        res = await google_top_link("python.org unittest")
        ref = "https://docs.python.org/3/library/unittest.html"
        self.assertEqual(res['url'], ref)

    async def test_google_top_link_fail(self):
        """Test google_top_link Fail (return None)."""
        res = await google_top_link("qsdfqdsfkqdmflkjdflj")
        self.assertIsNone(res)

    async def test_get_top_def(self):
        """Test UrbanSearch.get_top_def."""
        urban = UrbanSearch("Distro Hop")
        res = await urban.get_top_def()
        ref = "Distro Hop"
        self.assertEqual(res[0], ref)

    def test_youtube_top_link(self):
        """Test youtube_top_link."""
        res = youtube_top_link("epenser bohr")
        ref = "Bohr, l'étudiant troll - quickie 08 - e-penser"
        # print(res[0])
        self.assertEqual(res[0], ref)

    async def test_get_comicsblog(self):
        """Test get_comicsblog."""
        res = await get_comicsblog(1)[0]
        # print(res.find('title').text)
        self.assertIsNotNone(res)

    def test_get_gif(self):
        """Test get_gif."""
        gifs = GifJson("gifs.sample.json")
        my_gif = gifs.get_gif("your_gif_name")
        self.assertEqual(my_gif['url'], "your_gif_url")

    def test_get_gif_fail(self):
        """Test get_gif fail."""
        gifs = GifJson("gifs.sample.json")
        my_gif = gifs.get_gif("toto")
        self.assertIsNone(my_gif)  # gif toto return none

    async def test_getcomics_top_link_title(self):
        """Test getcomics_top_link (title only)."""
        title = await getcomics_top_link("Batman #79")[0]
        ref = "Batman #79 (2019)"
        self.assertEqual(title, ref)


if __name__ == '__main__':
    unittest.main()
