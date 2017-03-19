# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django_mb.handlers import apps
from django_mb.serializers import registry

from .serializers import serializer_factory  # noqa

logger = logging.getLogger(__name__)


def monitor_application(app_name):
    apps.append(app_name)


def register_serializer(model, serializer):
    registry[model] = serializer
