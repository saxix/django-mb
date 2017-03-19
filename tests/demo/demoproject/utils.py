# # -*- coding: utf-8 -*-
# import json
#
# from kafka import KafkaConsumer, TopicPartition
#
# from django_mb.config import config
#
#
# def consumer():
#     consumer = KafkaConsumer(bootstrap_servers=config["SERVER"],
#                              api_version=config["API_VERSION"],
#                              # client_id="pytest-client1",
#                              # auto_offset_reset="latest",
#                              enable_auto_commit=False,
#                              # max_poll_records=1,
#                              # group_id=config["GROUP"],
#                              # request_timeout_ms=40 * 1000,
#                              value_deserializer=lambda m: json.loads(m.decode("utf8")),
#                              # heartbeat_interval_ms=3 * 1000,
#                              # session_timeout_ms=30 * 1000,
#                              consumer_timeout_ms=20 * 1000,
#                              )
#     consumer.assign([TopicPartition(config["TOPIC"], 0)])
#     consumer.seek_to_beginning()
#
#     return consumer
