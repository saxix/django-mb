# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from ..lru_cache import lru_cache  # noqa

# from django.utils.functional import SimpleLazyObject

from django_mb.config import config

logger = logging.getLogger(__name__)


@lru_cache(1)
def get_producer():
    if config["BROKER"] == "kafka":
        from .kafka import Client
    elif config["BROKER"] == "rabbitmq":
        from .rabbit import Client
    else:
        raise Exception("Invalid broker '{}'".format(config['BROKER']))
    return Client()


# producer = SimpleLazyObject(get_producer)
