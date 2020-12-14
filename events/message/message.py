# pylint: disable=no-name-in-module
""" MESSAGE """

from flask import request
from library.common import Common
from flask_socketio import SocketIO, emit

try:

    from __main__ import SOCKETIO

except ImportError:

    from app import SOCKETIO

@SOCKETIO.on('message')
def message(json):
    """ Message """

    clients = []
    clients.append(request.sid)
    print('Message recived my event: ' + str(json))

    if json['token'] == '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed':

        response = {'user_name': "Bot", 'message': "Hello!"}
        emit('my response', json, room=clients[0])
        emit('my response', response, room=clients[0])

    else:

        response = {}
        response['status'] = 'Failed'
        response['alert'] = 'Invalid data!'
        emit('my response', response, room=clients[0])
