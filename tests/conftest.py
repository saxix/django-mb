# from __future__ import unicode_literals
import logging
import warnings
from collections import defaultdict

import pytest

from django_mb.config import config
from django_mb.producers.kafka import Client

logger = logging.getLogger("test")
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

# docker run -p 2181:2181 -p 9092:9092
#               --env ADVERTISED_HOST=`docker-machine ip \`docker-machine active\``
#               --env ADVERTISED_PORT=9092 spotify/kafka

levelNames = {
    logging.CRITICAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "NOTSET",
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


class Producer(Client):
    def __init__(self, **configs):
        self.messages = defaultdict(lambda: [])

    def _send(self, data):
        self.messages[config["TOPIC"]].append(data)


@pytest.fixture()
def producer(monkeypatch):
    p = Producer()
    # monkeypatch.setattr("django_mb.client.producer", producer)
    # monkeypatch.setattr("django_mb.handlers.producer", producer)
    return p


@pytest.fixture()
def target():
    from demoproject.models import DemoModel1
    return DemoModel1.objects.create(name="aaa")


def pytest_addoption(parser):
    parser.addoption("--log", default=None, action="store",
                     dest="log_level",
                     help="enable console log")

    parser.addoption("--log-add", default="", action="store",
                     dest="log_add",
                     help="add package to log")

    parser.addoption("--lazy", default=False, action="store_true",
                     dest="lazy",
                     help="Do not start docker containers")

    parser.addoption("--kafka-port", default=9092, action="store",
                     dest="kafka",
                     help="Kafka server")

    parser.addoption("--rabbit-port", default=5672, action="store",
                     dest="rabbit",
                     help="RabbitMQ server port")


def pytest_configure(config):
    warnings.simplefilter("once", DeprecationWarning)

    if config.option.log_level:
        import logging
        level = config.option.log_level.upper()
        assert level in levelNames.keys()
        format = "%(levelname)-7s %(name)-30s %(funcName)-20s:%(lineno)3s %(message)s"
        formatter = logging.Formatter(format)

        handler = logging.StreamHandler()
        handler.setLevel(levelNames[level])
        handler.setFormatter(formatter)

        for app in ["test", "demoproject", "django_mb"]:
            l = logging.getLogger(app)
            l.setLevel(levelNames[level])
            l.addHandler(handler)

        if config.option.log_add:
            for pkg in config.option.log_add.split(","):
                l = logging.getLogger(pkg)
                l.setLevel(levelNames[level])
                l.addHandler(handler)

    logger.info("pytest configured")
