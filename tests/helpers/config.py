# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

KAFKA = {"BROKER": "kafka",
         "SERVER": "localhost:9092"
         }
RABBIT = {"BROKER": "rabbitmq",
          "AUTH": {
              "USERNAME": "user",
              "PASSWORD": "password",
          },
          # "OPTIONS": {
          #     "API_VERSION": ""
          # }
          }
