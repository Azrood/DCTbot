#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Logging configuration."""

import json
import logging
import logging.config
from pathlib import Path


def setup_logging(
    default_path=Path('logging.json'),
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    if path.exists():
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
