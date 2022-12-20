from kafka import KafkaConsumer, KafkaProducer


consumer = KafkaConsumer('test_topic')


consumer.poll(10)