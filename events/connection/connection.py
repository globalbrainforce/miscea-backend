
""" CONNECTION """

from flask import request
from library.common import Common
from library.utils import Utils
from flask_socketio import SocketIO, emit

try:

    from __main__ import SOCKETIO

except ImportError:

    from app import SOCKETIO

utils = Utils()

@SOCKETIO.on('connect')
def connect():
    """ CONNECT """

    utils.data_log(divider=True)
    utils.data_log(data='Client Connected!')
    utils.data_log(data="Client ID: {0}".format(request.sid))
    utils.data_log(divider=True)

    emit('my response', {'data': 'Connected'})
    response = {'top_id': "Bot", 'message': "Client " + str(request.sid) + " connected!"}
    emit('chats', response, broadcast=True)

@SOCKETIO.on('disconnect')
def disconnect():
    """ DISCONNECT """
    response = {'top_id': "Bot", 'message': "Client " + str(request.sid) + " disconnected!"}
    emit('chats', response, broadcast=True)

    utils.data_log(divider=True)
    utils.data_log(data='Client Disconnected!')
    utils.data_log(data="Client ID: {0}".format(request.sid))
    utils.data_log(divider=True)
