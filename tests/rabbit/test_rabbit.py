# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import pytest
from pika import PlainCredentials
from pika.exceptions import ProbableAuthenticationError

from demoproject.models import DemoModel1

from django_mb.config import NOTIFY_CREATE, NOTIFY_DELETE, NOTIFY_UPDATE, config
from django_mb.producers.rabbit import Client
from helpers.config import RABBIT

logger = logging.getLogger("test.rabbit")

#
# @pytest.mark.django_db(transaction=True)
# def test_create(topic_rabbit, monkeypatch):
#     monkeypatch.setitem(config, "NOTIFY", NOTIFY_CREATE)
#     topic_name, c = topic_rabbit
#
#     target = DemoModel1.objects.create(name="aaa")
#     target.save()
#
#     logger.debug("Reading RabbitMQ topic '{}'".format(config["TOPIC"]))
#
#     c.start_consuming()
#     msg = c.message
#
#     assert msg["version"] == 1
#     assert msg["event"] == "create"
#     result = DemoModel1(**msg["payload"]["data"])
#     assert result.pk == target.pk
#     assert result == target

#
# @pytest.mark.django_db(transaction=True)
# def test_update(topic_rabbit, target, monkeypatch):
#     monkeypatch.setitem(config, "NOTIFY", NOTIFY_UPDATE)
#
#     topic_name, c = topic_rabbit
#
#     target.name = "bbb"
#     target.save()
#     assert DemoModel1.objects.filter(name="bbb").exists()
#
#     # with contextlib.closing(c):
#     logger.debug("Reading topic '{}'".format(config["TOPIC"]))
#     c.start_consuming()
#     msg = c.message
#
#     assert msg["version"] == 1
#     assert msg["event"] == "update", msg
#     assert DemoModel1(**msg["payload"]["data"]) == target
#
#
# @pytest.mark.django_db(transaction=True)
# def test_delete(topic_rabbit, target, monkeypatch):
#     monkeypatch.setitem(config, "NOTIFY", NOTIFY_DELETE)
#     topic_name, c = topic_rabbit
#
#     pk = target.pk
#     target.delete()
#
#     logger.debug("Reading topic '{}'".format(config["TOPIC"]))
#     c.start_consuming()
#     msg = c.message
#
#     assert msg["version"] == 1
#     assert msg["event"] == "delete"
#     assert msg["payload"]["data"]["id"] == pk, pk


def test_close(monkeypatch):
    monkeypatch.setitem(config, "AUTH", RABBIT["AUTH"])

    c = Client()
    assert c.producer.is_open
    c.producer.close()
    assert not c.producer.is_open
#
#
# def test_producer_cached_property():
#     # just to be sure to revert some "debugging code"
#     c = Client()
#     assert id(c.producer) == id(c.producer)
#

def test_credentials(settings):
    settings.MB = {"SERVER": "localhost:5672"}
    c = Client()
    with pytest.raises(ProbableAuthenticationError):
        assert c.producer.is_open

    settings.MB = {"BROKER": "rabbitmq",
                   "AUTH": {"USERNAME": "user",
                            "PASSWORD": "password",
                            }
                   }
    c = Client()
    assert c.producer.is_open
