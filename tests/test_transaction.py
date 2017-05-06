# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import pytest
from django.db.transaction import atomic, rollback

from demoproject.models import DemoModel1

from django_mb.config import NOTIFY_CREATE, config

logger = logging.getLogger("test")


@pytest.mark.django_db(transaction=True)
def test_transaction(mocker, monkeypatch):
    p = mocker.patch("django_mb.handlers.send_to_broker")
    monkeypatch.setitem(config, "NOTIFY", NOTIFY_CREATE)

    try:
        with atomic():
            target = DemoModel1(name="aaa")
            target.save()
            raise Exception
    except:
        rollback()
    assert not DemoModel1.objects.filter(name="aaa").exists()
    assert not p.called
