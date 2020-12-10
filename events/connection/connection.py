# pylint: disable=no-name-in-module
""" CONNECTION """

from flask import request
from library.common import Common
from flask_socketio import SocketIO, emit
# from __main__ import SOCKETIO

@SOCKETIO.on('connect')
def connect():
    """ CONNECT """
    print("ARGS: ", request.args)
    print("ARGS: ", request.sid)
    emit('my response', {'data': 'Connected'})

@SOCKETIO.on('disconnect')
def disconnect():
    """ DISCONNECT """
    print('Client disconnected')
    print("ARGS: ", request.sid)
