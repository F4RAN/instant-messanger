from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

sio = SocketIO(app)
sio.init_app(app, cors_allowed_origins="*")


@sio.on('message')
def handle_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
    sio.run(app , port=5000)
