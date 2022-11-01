from flask import request

class GeneralController:
    def connect(self):
        print(f'{request.sid} connected')

    def disconnect(self):
        print(f'{request.sid} disconnected')