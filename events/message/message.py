""" MESSAGE """
import json
import time
import asyncio

async def message(websocket, data):

    if not 'token' in data.keys():

        message = {}
        message['type'] = 'message'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    if data['token'] == '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed':

        message = {}
        message['type'] = 'message'
        message['status'] = 'ok'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 1

    else:

        message = {}
        message['type'] = 'message'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0








# # pylint: disable=no-name-in-module
# """ MESSAGE """

# from flask import request
# from library.common import Common
# from library.utils import Utils
# from flask_socketio import SocketIO, emit

# try:

#     from __main__ import SOCKETIO

# except ImportError:

#     from app import SOCKETIO

# utils = Utils()

# @SOCKETIO.on('message')
# def message(json):
#     """ Message """

#     clients = []
#     clients.append(request.sid)
#     utils.data_log(divider=True)
#     utils.data_log('Message recived: {0}'.format(json))
#     utils.data_log(divider=True)

#     if json['token'] == '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed':

#         response = {'top_id': "Bot", 'message': "Message received: " + str(json['message'])}
#         emit('my response', json, room=clients[0])
#         emit('my response', response, room=clients[0])
#         emit('chats', json, broadcast=True)

#     else:

#         response = {}
#         response['status'] = 'Failed'
#         response['alert'] = 'Invalid data!'
#         emit('my response', response, room=clients[0])
