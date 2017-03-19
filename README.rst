==============================
Django Message Broker Producer
==============================

.. image:: https://badge.fury.io/py/django-mb.png
    :target: https://badge.fury.io/py/django-mb

.. image:: https://travis-ci.org/saxix/django-mb.png?branch=master
    :target: https://travis-ci.org/saxix/django-mb

Django app to send updates/creations/deletions to a message broker.

Currently Kafka and RabbitMQ are supported.


Documentation
-------------

The full documentation is at https://django-mb.readthedocs.org.

Quickstart
----------

Install Django Message Broker Producer   ::

    pip install django-mb

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_mb.apps.DjangoMqConfig',
        ...
    )


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Features
--------

    - Use django signals mechanism. No custom code needed
    - Respect transactions. Only send messages if database transaction successed
    - Custom serialization


Todo
----
    - Two-Phase Commit protocol support
    - Handle broker Security


Links
~~~~~

+--------------------+----------------+--------------+------------------------+
| Stable             | |master-build| | |master-cov| |                        |
+--------------------+----------------+--------------+------------------------+
| Development        | |dev-build|    | |dev-cov|    |                        |
+--------------------+----------------+--------------+------------------------+
| Project home page: | https://github.com/saxix/django-mb                     |
+--------------------+---------------+----------------------------------------+
| Issue tracker:     | https://github.com/saxix/django-mb/issues?sort         |
+--------------------+---------------+----------------------------------------+
| Download:          | http://pypi.python.org/pypi/django-mb/                 |
+--------------------+---------------+----------------------------------------+
| Documentation:     | https://django-mb.readthedocs.org/en/latest/           |
+--------------------+---------------+--------------+-------------------------+

.. |master-build| image:: https://secure.travis-ci.org/saxix/django-mb.png?branch=master
                    :target: http://travis-ci.org/saxix/django-mb/

.. |master-cov| image:: https://coveralls.io/repos/saxix/django-mb/badge.svg?branch=master&service=github
            :target: https://coveralls.io/github/saxix/django-mb?branch=master


.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-mb.png?branch=develop
                  :target: http://travis-ci.org/saxix/django-mb/

.. |dev-cov| image:: https://coveralls.io/repos/saxix/django-mb/badge.svg?branch=develop&service=github
        :target: https://coveralls.io/github/saxix/django-mb?branch=develop

