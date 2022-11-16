from flask import Flask, request
from flask_socketio import SocketIO,emit
from sockets.v1.socket import routes
from config.mongo import connectIt

connectIt()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

sio = SocketIO(app)
sio.init_app(app, cors_allowed_origins="*")
routes(sio)






@sio.on('message')
def handle_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
    sio.run(app , port=5000)
