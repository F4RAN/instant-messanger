from json import dumps
from time import sleep

from flask import Flask, request
from flask_socketio import SocketIO, emit

from config.kafka_class import KafkaClass
from sockets.v1.socket import routes
from config.mongo import connectIt
from kafka import KafkaConsumer, KafkaProducer



connectIt()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

sio = SocketIO(app, logger=True, manage_session=False)
sio.init_app(app, cors_allowed_origins="*")
routes(sio)




# consumer = KafkaConsumer('test_topic')
# for msg in consumer:
#     print(msg)


if __name__ == '__main__':
    sio.run(app, port=5000)
