#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""
from pathlib import Path

# import aiohttp
import pytest
# from unittest.mock import MagicMock
# import asynctest
import googleapiclient.discovery
from googleapiclient.http import RequestMockBuilder

from cogs.youtube import youtube_top_link


DATA_DIR = Path(__file__).parent / "data"


def datafile(filename: str) -> Path:
    return DATA_DIR / filename


@ pytest.fixture
def api_discovery_json() -> str:
    with open(datafile("discovery.json"), encoding='utf-8') as f:
        content = f.read()
    return content


def test_youtube_top_link(monkeypatch, api_discovery_json):
    """Test youtube_top_link."""

    #  TODO: maybe use a fixture or a decorator ??
    def mock_build(*args, **kwargs):
        response = open(datafile("youtube1_resp.json"), encoding='utf-8').read()  # noqa: E501

        requestBuilder = RequestMockBuilder({'youtube.search.list': (None, response)})  # noqa: E501

        mockb = googleapiclient.discovery.build_from_document(
            api_discovery_json, developerKey="dummy",
            requestBuilder=requestBuilder)
        return mockb

    # We monkey patch googleapiclient.discovery.build, to create fake one
    monkeypatch.setattr(googleapiclient.discovery, "build", mock_build)

    res = youtube_top_link("epenser bohr")[0]

    ref = "Bohr, l'étudiant troll - quickie 08 - e-penser"
    assert res == ref


def test_youtube_top_playlist(monkeypatch, api_discovery_json):
    """Test youtube_top_link."""

    #  TODO: maybe use a fixture or a decorator ??
    def mock_build(*args, **kwargs):
        response = open(datafile("youtube2_resp.json")).read()

        requestBuilder = RequestMockBuilder({'youtube.search.list': (None, response)})  # noqa: E501

        mockb = googleapiclient.discovery.build_from_document(
            api_discovery_json, developerKey="dummy",
            requestBuilder=requestBuilder)
        return mockb

    # We monkey patch googleapiclient.discovery.build, to create fake one
    monkeypatch.setattr(googleapiclient.discovery, "build", mock_build)

    res, _ = youtube_top_link("Playlist Learning to Code with Python")

    ref = "Learning to Code with Python"
    assert res == ref


def test_youtube_top_channel(monkeypatch, api_discovery_json):
    """Test youtube_top_link with channel resp."""

    #  TODO: maybe use a fixture or a decorator ??
    def mock_build(*args, **kwargs):
        response = open(datafile("youtube3_resp.json")).read()

        requestBuilder = RequestMockBuilder({'youtube.search.list': (None, response)})  # noqa: E501

        mockb = googleapiclient.discovery.build_from_document(
            api_discovery_json, developerKey="dummy",
            requestBuilder=requestBuilder)
        return mockb

    # We monkey patch googleapiclient.discovery.build, to create fake one
    monkeypatch.setattr(googleapiclient.discovery, "build", mock_build)

    res, _ = youtube_top_link("Chaine Joueur du Grenier")

    ref = "Joueur Du Grenier"
    assert res == ref
