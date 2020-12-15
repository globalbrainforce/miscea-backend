
""" CONNECTION """

from flask import request
from library.common import Common
from flask_socketio import SocketIO, emit

try:

    from __main__ import SOCKETIO

except ImportError:

    from app import SOCKETIO

@SOCKETIO.on('connect')
def connect():
    """ CONNECT """
    print("*"*100)
    print('Client Connected!')
    print("ARGS: ", request.sid)
    emit('my response', {'data': 'Connected'})
    print("*"*100)

    x = 'Client Connected!'
    with open('/home/admin/miscea-backend/logs.txt',"a+") as output_file:
        output_file.write('{0}\n'.format(x))

@SOCKETIO.on('disconnect')
def disconnect():
    """ DISCONNECT """
    print("*"*100)
    print('Client Disconnected!')
    print("ARGS: ", request.sid)
    print("*"*100)
