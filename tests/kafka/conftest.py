# -*- coding: utf-8 -*-
import json
import logging
import time
from collections import defaultdict

import pytest
from kafka import KafkaConsumer, TopicPartition

from django_mb.config import config
from django_mb.producers.kafka import Client

logger = logging.getLogger("test")


# docker run -p 2181:2181 -p 9092:9092
#               --env ADVERTISED_HOST=`docker-machine ip \`docker-machine active\``
#               --env ADVERTISED_PORT=9092 spotify/kafka

@pytest.fixture(autouse=True, scope="function")
def broker(monkeypatch):
    logger.info("Set BROKER to kafka")
    from django_mb.producers.kafka import Client
    monkeypatch.setattr("django_mb.handlers.producer", Client())
    config["BROKER"] = "kafka"
    # config["SERVER"] = "localhost:9092"
    yield
    config["BROKER"] = ""


@pytest.fixture(autouse=False, scope="session")
def kafka(request):
    lazy = request.config.getoption("--lazy")
    if not lazy:
        import docker
        port = request.config.getoption("--kafka-port")

        client = docker.from_env()
        cfg = {"NUM_PARTITIONS": 1,
               "ZOOKEEPER": "localhost:2181",
               "AUTO_CREATE_TOPICS": "true",
               "ADVERTISED_HOST": "localhost",
               "ADVERTISED_PORT": port,
               }
        c = client.containers.create("spotify/kafka",
                                     detach=True,
                                     ports={port: port},
                                     environment=cfg)

        logger.info("Kafka starting: {}".format(cfg))
        c.start()
        timeout = time.time() + 10
        while (c.logs().find(b"kafka entered RUNNING state") < 0):
            time.sleep(1)
            if time.time() > timeout:
                raise Exception("Timeout waiting Kafka to start")
        logger.info("Kafka started")
    yield

    if not lazy:
        c.stop()
        c.remove()


@pytest.fixture(autouse=False, scope="function")
def topic(kafka, monkeypatch):
    topic_name = str(time.time())
    monkeypatch.setitem(config, "TOPIC", topic_name)

    consumer = KafkaConsumer(bootstrap_servers=config["SERVER"],
                             api_version=config["OPTIONS"]["API_VERSION"],
                             # client_id="pytest-client1",
                             # auto_offset_reset="latest",
                             enable_auto_commit=False,
                             # max_poll_records=1,
                             # group_id=config["GROUP"],
                             # request_timeout_ms=40 * 1000,
                             value_deserializer=lambda m: json.loads(m.decode("utf8")),
                             # heartbeat_interval_ms=3 * 1000,
                             # session_timeout_ms=30 * 1000,
                             consumer_timeout_ms=20 * 1000,
                             )
    consumer.assign([TopicPartition(topic_name, 0)])
    consumer.seek_to_beginning()
    logger.info("Created Kafka consumer and assigned to '{}'".format(topic_name))

    return topic_name, consumer


class Producer(Client):
    def __init__(self, **configs):
        self.messages = defaultdict(lambda: [])

    def _send(self, data):
        self.messages[config["TOPIC"]].append(data)
