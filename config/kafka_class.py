import json

from kafka import KafkaProducer, KafkaConsumer


class KafkaClass:
    TOPIC_NAME = "MESSAGES"
    KAFKA_SERVER = "localhost:9092"

    def get_producer(self):
        return self.producer

    def get_topic(self):
        return self.TOPIC_NAME

    def create_producer(self):
        return KafkaProducer(
            bootstrap_servers=self.KAFKA_SERVER,
        )

    def create_consumer(self):
        return KafkaConsumer(
            'MESSAGES',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            group_id="chat",
            consumer_timeout_ms=200
        )
