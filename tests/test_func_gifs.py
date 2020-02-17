#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import pytest  # noqa: F401

from utils.gif_json import GifJson


def test_get_gif():
    """Test get_gif."""
    gifs = GifJson("gifs.sample.json")
    my_gif = gifs.get_gif("your_gif_name")
    assert my_gif['url'] == "your_gif_url"


def test_get_gif_fail():
    """Test get_gif fail."""
    gifs = GifJson("gifs.sample.json")
    my_gif = gifs.get_gif("toto")
    assert my_gif is None  # gif toto return none


def test_get_names_string():
    """Test get_gif fail."""
    gifs_json = GifJson("gifs.sample.json")
    # gif_json_mock = MagicMock(GifJson)
    gifs_json.gifs = {"foo": {"public": True,
                              "url": "https://foo.gif"},
                      "bar": {"public": True,
                              "url": "http://bar.gif"},
                      "foobar": {"public": True,
                                 "url": "http://bar.gif"}
                      }
    gif_string = gifs_json.get_names_string(private=False)
    assert gif_string == "foo\nbar\nfoobar"


def test_get_names_string_private():
    """Test get_gif fail."""
    gifs_json = GifJson("gifs.sample.json")
    # gif_json_mock = MagicMock(GifJson)
    gifs_json.gifs = {"foo": {"public": True,
                              "url": "https://foo.gif"},
                      "bar": {"public": True,
                              "url": "http://bar.gif"},
                      "fooba": {"public": False,
                                "url": "http://bar.gif"}
                      }
    gif_string = gifs_json.get_names_string(private=True)
    assert gif_string == "foo\nbar"
