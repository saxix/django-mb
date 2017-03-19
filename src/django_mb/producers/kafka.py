# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

from django.utils.functional import cached_property
from kafka import KafkaProducer

from django_mb.config import config
from django_mb.serializers import serialize

logger = logging.getLogger(__name__)


class Client(object):
    @cached_property
    def producer(self):
        cfg = self._get_client_config()
        logger.debug("Configured Kafka producer {}".format(cfg))
        return KafkaProducer(**cfg)

    def send(self, event, instance):
        self.producer
        data = self.serialize(instance)
        data["event"] = event
        self._send(data)
        logger.debug("Sent '{}' event to topic '{}'".format(event, config["TOPIC"]))

    def _send(self, data):
        self.producer.send(config["TOPIC"],
                           key=str(data["key"]).encode("utf8"),
                           value=data)
        self.producer.flush()

    def serialize(self, obj):
        return serialize(obj)

    def _get_client_config(self):
        return {
            # "value_serializer": lambda m: json.dumps(m),
            "value_serializer": lambda m: json.dumps(m).encode("utf8"),
            # "key_serializer": lambda v: bytes([v]),
            "acks": 1,
            # "client_id": config["CLIENT"],
            "bootstrap_servers": config["SERVER"],
            "api_version": config["OPTIONS"]["API_VERSION"],
            # "retries": config["RETRIES"],
            # "request_timeout_ms": 300000
        }
