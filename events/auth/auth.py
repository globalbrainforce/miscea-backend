# pylint: disable=no-name-in-module
""" AUTH """

from flask import request
from library.common import Common
from flask_socketio import SocketIO, emit

try:

    from __main__ import SOCKETIO

except ImportError:

    from app import SOCKETIO

@SOCKETIO.on('auth')
def auth(json):
    """ authentication """

    clients = []
    clients.append(request.sid)
    print("*"*100)
    print('Auth recived my event: ' + str(json))
    print("*"*100)

    if not 'token' in json.keys():

        response = {}
        response['status'] = 'Failed'
        response['alert'] = 'Invalid data!'
        emit('my response', response, room=clients[0])

    if json['token'] == '269c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ec':

        response = {}
        response['status'] = 'ok'
        response['new_token'] = '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed'
        emit('my response', response, room=clients[0])
