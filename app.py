from flask import request
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

APP = Flask(__name__, template_folder='ui')
CORS(APP)

SOCKETIO = SocketIO(APP, cors_allowed_origins="*")

@SOCKETIO.on('connect')
def test_connect():
    """ CONNECT """
    print("ARGS: ", request.args)
    print("ARGS: ", request.sid)
    emit('my response', {'data': 'Connected'})

@SOCKETIO.on('disconnect')
def test_disconnect():
    """ DISCONNECT """
    print('Client disconnected')
    print("ARGS: ", request.sid)

def message_recived():
    """ RECEIVED MESSAGE """
    print('message was received!!!')

@SOCKETIO.on('token')
def handle_my_custom_event(json):
    """ HANDLE MESSAGE """
    clients = []
    clients.append(request.sid)
    print('recived my event: ' + str(json))
    json3 = {'user_name': "Bot", 'message': "Hello!"}
    SOCKETIO.emit('my response', json, callback=message_recived, room=clients[0])
    SOCKETIO.emit('my response', json3, callback=message_recived, room=clients[0])

@APP.route('/')
def home():
    """ HTML """
    return render_template('chat_ui.html')

if __name__ == '__main__':
    SOCKETIO.run(APP, host='0.0.0.0', debug=True)
