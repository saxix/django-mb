# -*- coding: utf-8
from django.apps import AppConfig

from django_mb.config import config


class DjangoMqConfig(AppConfig):
    name = "django_mb"

    def ready(self):
        import django_mb.handlers  # noqa
        from django_mb.api import monitor_application
        for app in config["APPS"]:
            monitor_application(app)
