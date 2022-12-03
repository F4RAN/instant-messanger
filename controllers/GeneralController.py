import json

import flask_socketio
import jwt
from flask import request
from app import emit
from models.socket import Socket
from models.user import User


class GeneralController:

    def check_friend_phone(self, params):
        user = User.objects(token=params['token']).first()
        friend = User.objects(phoneNumber=params['phoneNumber']).first()
        if not bool(friend): return emit('get_friend_info', {'status': False, 'exist': False, 'user': ''})
        for f in user.friends:
            print(f, friend.id)
            if f == str(friend.id): return emit('get_friend_info', {'status': True, 'exist': True, 'user': ''})
        user.friends.append(str(friend.id))
        user.save()
        user_schema = {'id': str(friend.id), 'name': friend.name, 'phoneNumber': friend.phoneNumber}
        user_schema = json.dumps(user_schema)
        user_schema = json.loads(user_schema)
        return emit('get_friend_info', json.loads(json.dumps({'status': True, 'exist': False, 'user': user_schema})))

    def get_friends(self):
        token = request.args.get('token')
        user = User.objects(token=token).first()
        friends_list = []
        for f in user.friends:
            friend = User.objects(id=f).first()
            friends_list.append({'id': str(friend.id), 'name': friend.name, 'phoneNumber': friend.phoneNumber})

        """ Messages assign to each friends later, to: user.id , from: friend.id or opposite"""
        return emit('friends_list', friends_list)

    def connect(self):
        token = request.args.get('token')
        # print(request.namespace.socket.sessid,"hello")
        print(f'{request.sid} connected')

        # User authentication
        user = False
        try:
            user = jwt.decode(token, "very_secure_secret", algorithms=["HS256"])
        except:
            pass
        if bool(user):
            check_socket = Socket.objects(sid=request.sid).first()
            my_user = User.objects(id=str(user['id'])).as_pymongo()
            if bool(check_socket):
                check_socket.is_connected = True
                check_socket.save()
            elif len(my_user) != 0:
                new_socket = Socket(sid=request.sid, userId=str(my_user[0]['_id']))
                new_socket.save()
            # Create common rooms between pair of friends
            for fr in my_user[0]['friends']:
                un = sorted((str(my_user[0]['_id']), str(fr)))
                flask_socketio.join_room(un[0] + un[1])

            if len(my_user) == 0: return emit('rejected')
            initial_data = {
                'name': my_user[0]['name'],
                'phone_number': my_user[0]['phoneNumber']
            }  # + friends list + latest 10 messages from all friends
            emit('accepted', initial_data)
        else:
            emit('rejected')

    def disconnect(self):
        print(f'{request.sid} disconnected')
