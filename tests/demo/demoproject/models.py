# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models


class DemoModel1(models.Model):
    name = models.CharField(max_length=200)
    integer = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        app_label = "demoproject"


class DemoModel2(models.Model):
    name = models.CharField(max_length=200)
    integer = models.IntegerField(default=0)
    date = models.DateField(auto_created=True, auto_now=True)

    class Meta:
        app_label = "demoproject"
