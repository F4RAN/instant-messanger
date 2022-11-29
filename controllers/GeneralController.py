import json

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
            print(f,friend.id)
            if f == str(friend.id): return emit('get_friend_info', {'status': True, 'exist': True, 'user': ''})
        user.friends.append(str(friend.id))
        user.save()
        return emit('get_friend_info', json.loads(json.dumps({'status': True,'exist':False, 'user': friend.name})))

    def connect(self):
        token = request.args.get('token')
        print(f'{request.sid} connected')

        # User authentication
        user = False
        try:
            user = jwt.decode(token, "very_secure_secret", algorithms=["HS256"])
        except:
            pass
        if bool(user):
            check_socket = Socket.objects(sid=request.sid).first()
            if bool(check_socket):
                check_socket.is_connected = True
                check_socket.save()
            else:
                new_socket = Socket(sid=request.sid)
                new_socket.save()
            my_user = User.objects(id=str(user['id'])).as_pymongo()
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
