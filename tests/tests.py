#!/usr/bin/python3
# -*-coding:utf-8 -*-


import unittest
from utils.tools import get_command_input
from utils.google import google_top_link
from utils.urban import Urban_search
from utils.youtube import youtube_top_link
from utils.comicsblog import get_comicsblog
from utils.gif_json import Gif_json


class TestDiscordBot(unittest.TestCase):
    """Run unit tests."""

    # Each method with name beginning with 'test_'
    # is a test.

    def test_get_command_input(self):
        input = get_command_input("!google python.org unittest")
        self.assertEqual(input, "python.org unittest")

    def test_google_top_link(self):
        res = google_top_link("python.org unittest")
        ref = "https://docs.python.org/3/library/unittest.html"
        self.assertEqual(res['url'], ref)

    def test_get_top_def(self):
        urban = Urban_search("Distro Hop")
        res = urban.get_top_def()
        print(res)
        assert res is not None

    def test_youtube_top_link(self):
        res = youtube_top_link("epenser bohr")
        print(res)
        assert res is not None

    def test_get_comicsblog(self):
        res = get_comicsblog(1)[0]
        print(res.find('title').text)

    def test_get_gif(self):
        gifs = Gif_json("utils/gifs.sample.json")
        my_gif = gifs.get_gif("your_gif_name")
        self.assertEqual(my_gif['url'], "your_gif_url")


if __name__ == '__main__':
    unittest.main()
