#!/usr/bin/env python
"""Provides a logging facility for structured log output."""

import logging
import logging.config
import time
import os
import json


def get_logger(name):
    """Return a Logger object that can be used to write structured logs.

    :param name: The name of the calling class.
    :param level: The logging level to import before the line."""
    logger = logging.getLogger(name)
    log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../logs/')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(name)s.%(levelname)s]: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": os.path.join(log_dir, "awsiamjson.log"),
                "encoding": "utf8",
                "maxBytes": 1048576,
                "backupCount": 10
            }
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": [
                    "console",
                    "file"
                ]
            }
        }
    })
    # Force all times to GMT and to use . as delimiter instead of ,
    for cur_handler in logging.getLogger().handlers:
        cur_handler.formatter.converter = time.gmtime
        cur_handler.formatter.default_msec_format = '%s.%03d'
    return logger


LOG = get_logger("iamwizard.awsiamjson")