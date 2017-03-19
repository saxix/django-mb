# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

NOTIFY_UPDATE = "update"
NOTIFY_CREATE = "create"
NOTIFY_DELETE = "delete"
NOTIFY_ALL = [NOTIFY_CREATE, NOTIFY_UPDATE, NOTIFY_DELETE]


def merge(a, b, path=None):
    """merges b into a

    >>> a={1:{"a":"A"},2:{"b":"B"}, 8:[]}
    >>> b={2:{"c":"C"},3:{"d":"D"}}

    >>> c = merge(a,b)
    >>> c == a == {8: [], 1: {u"a": u"A"}, 2: {u"c": u"C", u"b": u"B"}, 3: {u"d": u"D"}}
    True

    >>> c = merge(a, {1: "a"})
    Traceback (most recent call last):
        ...
    Exception: Conflict at 1
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


DEFAULTS = {"BROKER": "",
            "SERVER": "",
            "TOPIC": "topic",
            "GROUP": "django-mb",
            "RETRIES": 2,
            "NOTIFY": [],
            "TIMEOUT": 10,
            "APPS": [],
            "OPTIONS": {
                # kafka
                "API_VERSION": (0, 10),
                "CLIENT": "",
                "ACKS": 0,
                # rabbit
            },
            }

config = getattr(settings, "MB", {})

for key in DEFAULTS.keys():
    if key not in config:
        config[key] = DEFAULTS[key]
