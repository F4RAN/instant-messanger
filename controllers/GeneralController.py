from flask import request
from app import emit

class GeneralController:
    def connect(self):
        token = request.args.get('token')
        print(f'{request.sid} connected')
        if token == 'very_strong_token':
            print('here')
            emit('accepted')
        else:
            emit('rejected')


    def disconnect(self):
        print(f'{request.sid} disconnected')