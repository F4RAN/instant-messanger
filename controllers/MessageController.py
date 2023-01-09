import datetime
import json
import threading
from queue import Queue
import flask_socketio
from bson import json_util
from flask import request
from kafka import KafkaConsumer
from mongoengine import Q

from app import emit
from config.kafka_class import KafkaClass
from models.message import Message
from models.socket import Socket
from models.user import User
import jwt

kafka_class = KafkaClass()
topic = KafkaClass().get_topic()


def check_spam(message, msgs, time_limit):
    return message.created - msgs[5]['created'] < datetime.timedelta(seconds=time_limit)


class MessageController:



    def send_message(self, params):
        # Process message and some cencorship here
        token = request.args.get('token')
        fr = User.objects(token=token).first()
        msgs = Message.objects(f=str(fr.id)).order_by('-created')[0:5]
        to = User.objects(id=params['to']).first()
        swears = ["bi adab", "avazi", "namard", "ahmaq", "bi pedar", "ahmagh", "sag", "khar", "olagh", "olaq"]
        producer = kafka_class.create_producer()
        words_count = len(params['message'].split(" "))
        message = Message(f=str(fr.id), t=str(to.id),words_count=str(words_count), content=params['message'])
        if check_spam(message, msgs, 5):
            return emit("spam_detection")
        message.save()
        for index, word in enumerate(params['message'].split(" ")):
            producer.send(topic, bytes(word, "utf-8"), key=bytes(str(message.id) + "|||" + str(index), "utf-8"))
            producer.flush()
        producer.close(timeout=200)
        consumer = KafkaConsumer('MESSAGES',
                                 group_id='chat',
                                 bootstrap_servers=['localhost:9092'])
        msg_pack = consumer.poll(timeout_ms=1000)
        for tp, messages in msg_pack.items():
            for word in messages:
                id = word.key.decode("utf-8").split("|||")[0]
                s = word.value.decode("utf-8")
                if s in swears:
                    msg = Message.objects(id=id).first()
                    msg.content = msg.content.replace(s, "****")
                    msg.save()


        # for word in consumer:
        #     print("here")
        #     # consumer.commit()
        #     s = word.value.decode("utf-8")
        #     print(word.key,word.value)
        #     i = word.key.decode("utf-8").split("|||")[1]
        #     i = int(i)
        #     id = word.key.decode("utf-8").split("|||")[0]
        #     last_s = s
        #     print(s)
        #     if s in swears:
        #         s = len(s) * "*"
        #         msg = Message.objects(id=id).first()
        #         msg.content = msg.content.replace(last_s,s)
        #         msg.save()



        consumer.close(autocommit=True)
        msg = Message.objects(id=str(message.id)).first()
        # filtered_message =  " ".join(result)
        msg_schema = {
            'id': str(message.id),
            'message': msg.content,
            'from': str(fr.id),
            'seen': False,
            'created': str(message.created),
            'to': 'me'
        }
        un = sorted((str(fr.id), str(to.id)))
        try:
            emit("receive_message", json.loads(json.dumps(msg_schema)), room=un[0] + un[1], include_self=False)
        except:
            pass
        msg_schema = {
            'id': str(message.id),
            'message': msg.content,
            'from': 'me',
            'index': params['index'],
            'all_index': params['index'],
            'created': str(message.created),
            'to': str(fr.id),
        }
        emit("message_sent", json.loads(json.dumps(msg_schema)))

    def get_messages_history(self):
        token = request.args.get('token')
        me = User.objects(token=token).first()
        print(str(me.id))
        messages = Message.objects.filter(Q(t=str(me.id)) | Q(f=str(me.id))).order_by('created').as_pymongo()
        counter = 0
        history_schema = []
        # Limit messages per user
        limitation_value = 10
        print(messages)
        for friend in me.friends:
            for i in range(len(messages)):
                if messages[len(messages) - 1 - i]['t'] == friend or messages[len(messages) - 1 - i]['f'] == friend:
                    counter += 1
                    history_schema.append(messages[len(messages) - 1 - i])
                if counter == limitation_value:
                    break

            counter = 0
        emit('messages_history', json.loads(json_util.dumps(reversed(history_schema))))

    def seen_friend_messages(self, fr_id):
        token = request.args.get('token')
        me = User.objects(token=token).first()
        # Seen all messages from this friend (id) to me
        msgs = Message.objects(f=fr_id, t=str(me.id))
        for msg in msgs:
            msg.seen = True
            msg.save()
        fr = fr_id
        to = str(me.id)
        un = sorted((str(fr), str(to)))
        emit('friend_seen', to, room=un[0] + un[1])

    def seen_message(self, params):
        msg = Message.objects(id=params['id']).first()
        msg.seen = True
        msg.save()
        un = sorted((str(msg.f), str(msg.t)))
        emit('double_check', params['id'], room=un[0] + un[1])
