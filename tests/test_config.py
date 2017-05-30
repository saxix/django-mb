# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from django_mb.config import config, DEFAULTS


def test_config(settings):
    settings.MB = {}
    assert config == DEFAULTS != settings.MB
    assert id(config) != id(DEFAULTS) != id(settings.MB)


@pytest.mark.parametrize("broker", ["rabbit", "kafka"])
def test_parse_settings(broker, settings):
    settings.MB = {"BROKER": broker}
    assert config["BROKER"] == broker

