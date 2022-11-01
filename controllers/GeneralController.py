from flask import request
from app import emit

class GeneralController:
    def connect(self):
        print(f'{request.sid} connected')
        emit('accepted')

    def disconnect(self):
        print(f'{request.sid} disconnected')