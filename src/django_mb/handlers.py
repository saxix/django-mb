# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django_mb.config import NOTIFY_CREATE, NOTIFY_DELETE, NOTIFY_UPDATE, config
from django_mb.producers import get_producer

logger = logging.getLogger(__name__)

apps = []


@receiver(post_save, dispatch_uid="django_mb_register_update")
def register_update(sender, instance, raw, created, **kwargs):
    if sender._meta.app_label not in apps:
        return
    op = {True: NOTIFY_CREATE, False: NOTIFY_UPDATE}[created]
    if op not in config["NOTIFY"]:
        return
    logger.debug("Add '{}' event for '{}'".format(op, instance))
    transaction.on_commit(lambda: send_to_broker(op, instance))


@receiver(post_delete, dispatch_uid="django_mb_register_deletion")
def register_deletion(sender, instance, **kwargs):
    if sender._meta.app_label not in apps:  # pragma: no-cover
        return
    if NOTIFY_DELETE not in config["NOTIFY"]:
        return
    logger.debug("Add 'delete' event for '{}'".format(instance))
    transaction.on_commit(lambda: send_to_broker(NOTIFY_DELETE, instance))


def send_to_broker(op, instance):
    logger.debug("Processing '{}' event for '{}'".format(op, instance))
    get_producer().send(op, instance)
