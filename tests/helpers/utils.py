# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pika
import pytest
import time

from kafka import KafkaConsumer as KafkaConsumerOrig, TopicPartition
from pika import PlainCredentials

from demoproject.models import DemoModel1
from django_mb.config import config, NOTIFY_CREATE, NOTIFY_UPDATE, NOTIFY_DELETE

import logging

from helpers.config import RABBIT

logger = logging.getLogger("test.helppers")


class RabbitConsumer(object):
    def __init__(self, topic_name, port):
        self.topic_name = topic_name
        cfg = {"host": "localhost",
               "credentials": PlainCredentials(RABBIT["AUTH"]["USERNAME"],
                                               RABBIT["AUTH"]["PASSWORD"]),
               "port": port,
               }
        conn = pika.BlockingConnection(pika.ConnectionParameters(**cfg))

        def on_timeout():
            conn.close()
            raise Exception("Timeout waiting Rabbit message")

        self.consumer = conn.channel()
        self.consumer.queue_declare(topic_name)
        conn.add_timeout(5, on_timeout)

    def __call__(self, ch, method, properties, body):
        ch.stop_consuming()
        self.message = json.loads(body.decode("utf8"))

    def start_consuming(self):
        self.consumer.basic_consume(self, queue=self.topic_name, no_ack=True)
        self.consumer.start_consuming()


class KafkaConsumer(KafkaConsumerOrig):
    @property
    def message(self):
        return next(self).value

    def start_consuming(self):
        pass


def kafka_env(settings, request):
    from django_mb.handlers import get_producer
    topic_name = str(time.time())

    get_producer.cache_clear()
    settings.MB = {"BROKER": "kafka",
                   "SERVER": "localhost:9092",
                   "TOPIC": topic_name
                   }

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


def rabbit_env(settings, request):
    topic_name = str(time.time())
    logger.info("Set BROKER to rabbitmq")
    from django_mb.handlers import get_producer
    get_producer.cache_clear()
    cfg = dict(RABBIT)
    cfg["TOPIC"] = topic_name
    settings.MB = cfg
    # settings.MB = {"BROKER": "rabbitmq",
    #                "TOPIC": topic_name,
    #                "AUTH": {
    #                    "USERNAME": "user",
    #                    "PASSWORD": "password",
    #                },
    #                }

    port = request.config.getoption("--rabbit-port")

    return topic_name, RabbitConsumer(topic_name, port)
