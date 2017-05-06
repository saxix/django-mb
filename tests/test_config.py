# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django_mb.config import config, DEFAULTS


def test_config(settings):
    settings.MB = {}
    assert config == DEFAULTS != settings.MB
    assert id(config) != id(DEFAULTS) != id(settings.MB)


def test_parse_settings(settings):
    settings.MB = {"BROKER": "kafka"}
    assert config["BROKER"] == "kafka"

    settings.MB = {"BROKER": "rabbit"}
    assert config["BROKER"] == "rabbit"
