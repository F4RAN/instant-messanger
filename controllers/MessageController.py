import json

import flask_socketio
from flask import request
from app import emit
from models.message import Message
from models.socket import Socket
from models.user import User
import jwt

class MessageController:
    def send_message(self,params):
        # Process message and some cencorship here
        token = request.args.get('token')
        fr = User.objects(token=token).first()
        to = User.objects(id=params['to']).first()
        dest_socket = Socket.objects(userId=str(to.id)).first()
        message = Message(f=str(fr.id) ,t=str(to.id), content=params['message'])
        message.save()
        msg_schema = {
            'message':params['message'],
            'from':str(fr.id),
            'to':'me'
        }
        un = sorted((str(fr.id), str(to.id)))
        emit("receive_message",json.loads(json.dumps(msg_schema)), room=un[0] + un[1] , include_self=False)
