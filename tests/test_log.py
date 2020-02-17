#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""


import pytest  # noqa: F401
from utils.logs import CommandLog


def test_log_read_0():  # case 0, [None, None, None]
    """Test log read."""
    date = "08/11/2019"
    arg_list = [None, None, None]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    assert len(res) == 5


def test_log_read_1():  # case 1, [None, None, channel]
    """Test log read."""
    date = "08/11/2019"
    arg_list = [None, None, "faq"]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    ref = ('23h07m12s', 'bart', 'kick')
    assert res[0] == ref


def test_log_read_2():  # case 2, [None, command, None]
    """Test log read."""
    date = "08/11/2019"
    arg_list = [None, "clear", None]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    assert len(res) == 3


def test_log_read_3():  # case 0, [None, command, channel]
    """Test log read."""
    date = "08/11/2019"
    arg_list = [None, "clear", "general"]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    ref = ('23h07m21s', 'lisa', 'clear')
    assert res[1] == ref


def test_log_read_4():  # case 4, [user, None, None]
    """Test log read."""
    date = "08/11/2019"
    arg_list = ["homer", None, None]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    assert len(res) == 2


def test_log_read_5():  # case 5, [user, None, channel]
    """Test log read."""
    date = "08/11/2019"
    arg_list = ["lisa", None, "faq"]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    ref = ('23h07m25s', 'lisa', 'clear')
    assert res[0] == ref


def test_log_read_6():  # case 6, [user, command, None]
    """Test log read."""
    date = "08/11/2019"
    arg_list = ["homer", "ban", None]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    ref = ('23h07m32s', 'homer', 'general')
    assert res[0] == ref


def test_log_read_7():  # case 7, [user, command, channel]
    """Test log read."""
    date = "08/11/2019"
    arg_list = ["bart", "kick", "faq"]
    logs = CommandLog("logs.sample.json")
    res = logs.log_read(date, *arg_list)
    # print(res)
    ref = ('08/11/2019', '23h07m12s')
    assert res[0] == ref
