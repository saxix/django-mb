# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import pytest

from demoproject.models import DemoModel2

from django_mb.api import register_serializer, serializer_factory
from django_mb.serializers import serialize

logger = logging.getLogger("test")


def test_serializer_factory():
    ser = serializer_factory(DemoModel2)
    assert ser(DemoModel2()).data == {u"id": None,
                                      "name": u"",
                                      "integer": 0,
                                      "date": None}

    ser1 = serializer_factory(DemoModel2, fields=["name"])
    assert ser1(DemoModel2()).data == {"name": u""}

    ser2 = serializer_factory(DemoModel2, exclude=["name"])
    assert ser2(DemoModel2()).data == {u"id": None, "integer": 0, "date": None}


@pytest.mark.django_db()
def test_custom_serializer():
    register_serializer(DemoModel2,
                        serializer_factory(DemoModel2, fields=["name"]))

    obj = DemoModel2.objects.create(name="aaa")

    msg = serialize(obj)
    assert msg["version"] == 1
    assert msg["payload"]["data"] == {u"name": u"aaa"}
