import json
import logging
import time

import pika
import pytest

from django_mb.config import config

logger = logging.getLogger("test.rabbit")


@pytest.fixture(autouse=True, scope="function")
def broker(monkeypatch):
    logger.info("Set BROKER to rabbitmq")
    # from django_mb.producers.rabbit import Client
    # monkeypatch.setattr("django_mb.handlers.producer", Client())
    from django_mb.handlers import get_producer
    get_producer.cache_clear()
    config["BROKER"] = "rabbitmq"
    yield
    config["BROKER"] = ""


@pytest.fixture(autouse=False, scope="session")
def rabbit(request):
    lazy = request.config.getoption("--lazy")
    if not lazy:
        import docker
        port = request.config.getoption("--rabbit-port")

        client = docker.from_env()
        c = client.containers.create("rabbitmq:3",
                                     detach=True,
                                     ports={
                                         port: port
                                     },
                                     environment={
                                     })
        logger.info("RabbitMQ starting.")
        c.start()
        timeout = time.time() + 10
        while (c.logs().find(b"Server startup complete") < 0):
            time.sleep(1)
            if time.time() > timeout:
                raise Exception("Timeout waiting RabbitMQ to start")
        logger.info("RabbitMQ started")
    yield

    if not lazy:
        c.stop()
        c.remove()


class Consumer(object):
    def __init__(self, topic_name, port):
        self.topic_name = topic_name
        # credentials = pika.PlainCredentials('guest', 'guest')
        conn = pika.BlockingConnection(pika.ConnectionParameters(**{"host": "localhost",
                                                                    "port": port,
                                                                    }))

        def on_timeout():
            conn.close()
            raise Exception("Timeout waiting Rabbit message")

        self.consumer = conn.channel()
        self.consumer.queue_declare(topic_name)
        conn.add_timeout(5, on_timeout)

    def __call__(self, ch, method, properties, body):
        ch.stop_consuming()
        self.message = json.loads(body.decode("utf8"))

    def start_consuming(self):
        self.consumer.basic_consume(self, queue=self.topic_name, no_ack=True)
        self.consumer.start_consuming()


@pytest.fixture(autouse=False, scope="function")
def topic_rabbit(rabbit, monkeypatch, request):
    topic_name = str(time.time())
    monkeypatch.setitem(config, "TOPIC", topic_name)
    port = request.config.getoption("--rabbit-port")

    return topic_name, Consumer(topic_name, port)
