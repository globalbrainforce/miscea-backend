from flask import request
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

APP = Flask(__name__)
CORS(APP)

SOCKETIO = SocketIO(APP)

def message_recived():
    """ RECEIVED MESSAGE """
    print('message was received!!!')

@SOCKETIO.on('token', namespace='/token')
def handle_my_custom_event(json):
    """ HANDLE MESSAGE """
    clients = []
    clients.append(request.sid)
    print('recived my event: ' + str(json))
    json3 = {'user_name': json['user_name'], 'message': "Hello!"}
    SOCKETIO.emit('my response', json3, callback=message_recived, room=clients[0])

if __name__ == '__main__':
    SOCKETIO.run(APP, host='0.0.0.0', debug=True)
