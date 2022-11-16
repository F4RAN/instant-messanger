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
            return emit("get_token", new_user.token)