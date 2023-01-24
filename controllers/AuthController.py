from flask import request
from app import emit
from models.socket import Socket
from models.user import User
import jwt

class AuthController:
    def register(self,params):
        user = User.objects(phoneNumber=params['phoneNumber']).first()
        if bool(user):
            return emit("get_token", user.token)
        else:
            new_user = User(name=params['name'], phoneNumber=params['phoneNumber'])
            new_user.save()
            encoded_jwt = jwt.encode({"id": str(new_user['id'])}, "very_secure_secret",algorithm="HS256")
            print(encoded_jwt)
            new_user['token'] = encoded_jwt
            new_user.save()
            emit("get_token", new_user.token)
            initial_data = {
                'id': str(new_user.id),
                'name': new_user.name,
                'phone_number': new_user.phoneNumber
            }
            new_socket = Socket(sid=request.sid, userId=str(new_user.id))
            new_socket.save()
            return emit("accepted",initial_data)