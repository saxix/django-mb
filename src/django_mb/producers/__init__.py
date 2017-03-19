# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.utils.functional import SimpleLazyObject

from django_mb.config import config

logger = logging.getLogger(__name__)


def get_producer():
    if config["BROKER"] == "kafka":
        from .kafka import Client
    elif config["BROKER"] == "rabbitmq":
        from .rabbit import Client

    return Client()


producer = SimpleLazyObject(get_producer)
