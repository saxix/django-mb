Configuration
=============

Configure
---------

::

    DEFAULTS = {"BROKER": "",
            "SERVER": "",
            "TOPIC": "topic",
            "GROUP": "django-mb",
            "RETRIES": 2,
            "NOTIFY": [],
            "TIMEOUT": 10,
            "APPS": [],
            "AUTH":{
                "USERNAME": "",
                "PASSWORD": "",
            },
            "OPTIONS": {
                # kafka
                "API_VERSION": (0, 10),
                "CLIENT": "",
                "ACKS": 0,
                # rabbit
                },
            }


RabbitMQ
--------


Kafka
-----
