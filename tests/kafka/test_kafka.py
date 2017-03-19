# -*- coding: utf-8 -*-
from __future__ import absolute_import

import contextlib
import logging

import pytest

from demoproject.models import DemoModel1

from django_mb.config import NOTIFY_CREATE, NOTIFY_DELETE, NOTIFY_UPDATE, config

logger = logging.getLogger("test.kafka")


@pytest.mark.django_db(transaction=True)
def test_create(topic, monkeypatch):
    monkeypatch.setitem(config, "NOTIFY", NOTIFY_CREATE)
    topic_name, c = topic

    target = DemoModel1(name="aaa")
    target.save()

    logger.debug("Reading Kafka topic '{}'".format(config["TOPIC"]))

    # with contextlib.closing(c):
    msg = next(c).value

    assert msg["version"] == 1, msg
    assert msg["event"] == "create"
    result = DemoModel1(**msg["payload"]["data"])
    assert result.pk == target.pk
    assert result == target


@pytest.mark.django_db(transaction=True)
def test_update(topic, target, monkeypatch):
    monkeypatch.setitem(config, "NOTIFY", NOTIFY_UPDATE)

    topic_name, c = topic

    target.name = "bbb"
    target.save()
    assert DemoModel1.objects.filter(name="bbb").exists()

    with contextlib.closing(c):
        logger.debug("Reading Kafka topic '{}'".format(config["TOPIC"]))
        msg = next(c).value

    assert msg["version"] == 1
    assert msg["event"] == "update", msg
    assert DemoModel1(**msg["payload"]["data"]) == target


@pytest.mark.django_db(transaction=True)
def test_delete(topic, target, monkeypatch):
    monkeypatch.setitem(config, "NOTIFY", NOTIFY_DELETE)
    topic_name, c = topic

    pk = target.pk
    target.delete()

    with contextlib.closing(c):
        logger.debug("Reading Kafka topic '{}'".format(config["TOPIC"]))
        msg = next(c).value

    assert msg["version"] == 1
    assert msg["event"] == "delete"
    assert msg["payload"]["data"]["id"] == pk, pk
