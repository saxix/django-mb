# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pika
from django.utils.functional import cached_property
from pika import PlainCredentials

from django_mb.config import config
from django_mb.serializers import serialize

logger = logging.getLogger(__name__)


class Client(object):
    @property
    def producer(self):
        cfg = self._get_client_config()
        logger.debug("RabbitMQ configuration {}".format(cfg))
        conn = pika.BlockingConnection(pika.ConnectionParameters(**cfg))
        channel = conn.channel()
        channel.queue_declare(queue=config["TOPIC"])
        logger.debug("Configured RabbitMQ producer on channel {}".format(config["TOPIC"]))

        return channel

    def send(self, event, instance):
        data = self.serialize(instance)
        data["event"] = event
        self._send(json.dumps(data))
        logger.debug("Sent '{}' event to topic '{}'".format(event, config["TOPIC"]))

    def _send(self, data):
        self.producer.basic_publish(exchange="",
                                    routing_key=config["TOPIC"],
                                    body=data)

    def __del__(self):
        if self.producer.is_open:
            self.producer.close()

    def serialize(self, obj):
        return serialize(obj)

    def _get_client_config(self):
        port = 5672
        if ":" in config["SERVER"]:
            host, port = config["SERVER"].split(":")
        else:
            host = config["SERVER"]
        return {"host": host or "localhost",
                "port": port,
                # "virtual_host": None,
                "credentials": PlainCredentials(config["AUTH"]["USERNAME"],
                                                config["AUTH"]["PASSWORD"]),
                # "channel_max": None,
                # "frame_max": None,
                # "heartbeat_interval": None,
                # "ssl": None,
                # "ssl_options": None,
                # "connection_attempts": None,
                # "retry_delay": None,
                # "socket_timeout": None,
                # "locale": None,
                # "backpressure_detection": None
                }
