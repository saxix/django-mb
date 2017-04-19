=====
Usage
=====

To use DjangoMB in a project::


    import django_mb


    INSTALLED_APPS = [
        ...
        "django_mb.apps.DjangoMqConfig",
        ...
        ]


    MB = {"SERVER": "localhost",
      "RETRIES": 10,
      "TIMEOUT": 10,
      "NOTIFY": [],
      "BROKER": "",
      "APPS": ["demoproject"]
      }
