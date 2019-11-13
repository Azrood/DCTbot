#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""


import unittest
from utils.logs import CommandLog


class TestLog(unittest.TestCase):
    """Run unit tests."""

    # Each method with name beginning with 'test_'
    # is a test.

    def test_log_read_0(self):  # case 0, [None, None, None]
        """Test log read."""
        date = "08/11/2019"
        arg_list = [None, None, None]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        self.assertEqual(len(res), 5)

    def test_log_read_1(self):  # case 1, [None, None, channel]
        """Test log read."""
        date = "08/11/2019"
        arg_list = [None, None, "faq"]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        ref = ('23h07m12s', 'bart', 'kick')
        self.assertEqual(res[0], ref)

    def test_log_read_2(self):  # case 2, [None, command, None]
        """Test log read."""
        date = "08/11/2019"
        arg_list = [None, "clear", None]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        self.assertEqual(len(res), 3)

    def test_log_read_3(self):  # case 0, [None, command, channel]
        """Test log read."""
        date = "08/11/2019"
        arg_list = [None, "clear", "general"]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        ref = ('23h07m21s', 'lisa', 'clear')
        self.assertEqual(res[1], ref)

    def test_log_read_4(self):  # case 4, [user, None, None]
        """Test log read."""
        date = "08/11/2019"
        arg_list = ["homer", None, None]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        self.assertEqual(len(res), 2)

    def test_log_read_5(self):  # case 5, [user, None, channel]
        """Test log read."""
        date = "08/11/2019"
        arg_list = ["lisa", None, "faq"]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        ref = ('23h07m25s', 'lisa', 'clear')
        self.assertEqual(res[0], ref)

    def test_log_read_6(self):  # case 6, [user, command, None]
        """Test log read."""
        date = "08/11/2019"
        arg_list = ["homer", "ban", None]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        ref = ('23h07m32s', 'homer', 'general')
        self.assertEqual(res[0], ref)

    def test_log_read_7(self):  # case 7, [user, command, channel]
        """Test log read."""
        date = "08/11/2019"
        arg_list = ["bart", "kick", "faq"]
        logs = CommandLog("logs.sample.json")
        res = logs.log_read(date, *arg_list)
        # print(res)
        ref = ('08/11/2019', '23h07m12s')
        self.assertEqual(res[0], ref)


if __name__ == '__main__':
    unittest.main()
