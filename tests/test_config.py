# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import pytest

from django_mb.config import merge

logger = logging.getLogger("test")


def test_config(settings):
    settings.KAFKA = {}


def test_merge():
    a = {1: {"a": "A"}, 2: {"b": "B"}, 8: []}
    b = {2: {"c": "C"}, 3: {"d": "D"}}

    c = merge(a, b)
    assert c == a == {8: [],
                      1: {u"a": u"A"},
                      2: {u"c": u"C", u"b": u"B"},
                      3: {u"d": u"D"}}

    with pytest.raises(Exception):
        c = merge(a, {1: "a"})

    c = merge(b, b)
    assert c == b
