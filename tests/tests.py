#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""


import unittest
from utils.tools import get_command_input
from utils.google import google_top_link
from utils.urban import UrbanSearch
from utils.youtube import youtube_top_link
from utils.comicsblog import get_comicsblog
from utils.gif_json import GifJson
from utils.getcomics import getcomics_top_link


class TestDiscordBot(unittest.TestCase):
    """Run unit tests."""

    # Each method with name beginning with 'test_'
    # is a test.

    def test_get_command_input(self):
        """Test split command and input."""
        input = get_command_input("!google python.org unittest")
        self.assertEqual(input, "python.org unittest")

    def test_google_top_link(self):
        """Test google_top_link."""
        res = google_top_link("python.org unittest")
        ref = "https://docs.python.org/3/library/unittest.html"
        self.assertEqual(res['url'], ref)

    def test_get_top_def(self):
        """Test UrbanSearch.get_top_def."""
        urban = UrbanSearch("Distro Hop")
        res = urban.get_top_def()
        print(res)
        assert res is not None

    def test_youtube_top_link(self):
        """Test youtube_top_link."""
        res = youtube_top_link("epenser bohr")
        print(res)
        assert res is not None

    def test_get_comicsblog(self):
        """Test get_comicsblog."""
        res = get_comicsblog(1)[0]
        print(res.find('title').text)

    def test_get_gif(self):
        """Test get_gif."""
        gifs = GifJson("utils/gifs.sample.json")
        my_gif = gifs.get_gif("your_gif_name")
        self.assertEqual(my_gif['url'], "your_gif_url")

    def test_getcomics_top_link_title(self):
        """Test getcomics_top_link (title only)."""
        title = getcomics_top_link("Batman #79")[0]
        ref = "Batman #79 (2019)"
        self.assertEqual(title, ref)


if __name__ == '__main__':
    unittest.main()
