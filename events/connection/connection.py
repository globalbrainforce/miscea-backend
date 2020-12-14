
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
    print("ARGS: ", request.args)
    print("ARGS: ", request.sid)
    emit('my response', {'data': 'Connected'})
    print("*"*100)

@SOCKETIO.on('disconnect')
def disconnect():
    """ DISCONNECT """
    print("*"*100)
    print('Client disconnected')
    print("ARGS: ", request.sid)
    print("*"*100)
