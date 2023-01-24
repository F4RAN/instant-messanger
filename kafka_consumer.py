import sys
from confluent_kafka import Consumer, KafkaError, KafkaException
from models.message import Message
from config.mongo import connectIt
connectIt()
f = open("words.csv", "r")
words = f.read()
words = words.split(",\n")
topic = "INSTANT"
running = True
MIN_COMMIT_COUNT = 1
conf = {'bootstrap.servers': 'localhost:9092',
        'group.id': "foo",
        'auto.offset.reset': 'earliest'}
consumer = Consumer(conf)


def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        msg_count = 0
        while running:
            msg = consumer.poll(timeout=0.5)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def msg_process(msg):
    id = msg.key().decode("utf-8").split("|||")[0]
    s = msg.value().decode("utf-8")
    if s in words:
        dbmsg = Message.objects(id=id).first()
        dbmsg.content = dbmsg.content.replace(s, len(s)*"*")
        dbmsg.save()


print("Kafka consumer started successfully.")
consume_loop(consumer, [topic])
