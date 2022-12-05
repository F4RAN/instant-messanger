import json

import flask_socketio
from flask import request
from app import emit
from models.message import Message
from models.socket import Socket
from models.user import User
import jwt


class MessageController:
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
        emit('friend_seen',to, room=un[0] + un[1])

    def seen_message(self, params):
        msg = Message.objects(id=params['id']).first()
        msg.seen = True
        msg.save()
        un = sorted((str(msg.f), str(msg.t)))
        emit('double_check', params['id'], room=un[0] + un[1])

    def send_message(self, params):
        # Process message and some cencorship here
        token = request.args.get('token')
        fr = User.objects(token=token).first()
        to = User.objects(id=params['to']).first()
        message = Message(f=str(fr.id), t=str(to.id), content=self.cencor_message(params['message']))
        message.save()
        msg_schema = {
            'id': str(message.id),
            'message': self.cencor_message(params['message']),
            'from': str(fr.id),
            'seen': False,
            'to': 'me'
        }
        un = sorted((str(fr.id), str(to.id)))
        emit("receive_message", json.loads(json.dumps(msg_schema)), room=un[0] + un[1], include_self=False)
        msg_schema = {
            'id': str(message.id),
            'message': self.cencor_message(params['message']),
            'from': 'me',
            'index': params['index'],
            'all_index': params['index'],
            'to': str(fr.id),
        }
        emit("message_sent", json.loads(json.dumps(msg_schema)))

    def cencor_message(self, param):
        x = param
        list = ['bi adab', 'bi sharaf', 'ahmaq', 'pedar sag', 'bi pedar', 'khar']
        for word in list:
            x = x.replace(word, "*****")
        return x
