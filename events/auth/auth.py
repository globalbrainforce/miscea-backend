""" AUTH """
import json
import asyncio

async def auth(websocket, data):

    message = json.dumps({"type": "state", "value": 10})

    if not 'token' in data.keys():

        message = {}
        message['type'] = 'state'
        message['value'] = 1
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    if data['token'] == '269c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ec':

        message = {}
        message['type'] = 'state'
        message['value'] = 100
        message['status'] = 'ok'
        message['new_token'] = '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 1

    else:

        message = {}
        message['type'] = 'state'
        message['value'] = 1
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0








# from flask import request
# from library.common import Common
# from flask_socketio import SocketIO, emit
# from library.utils import Utils

# try:

#     from __main__ import SOCKETIO

# except ImportError:

#     from app import SOCKETIO

# utils = Utils()

# @SOCKETIO.on('auth')
# def auth(json):
#     """ authentication """

#     clients = []
#     clients.append(request.sid)

#     utils.data_log(divider=True)
#     utils.data_log('Auth recived: {0}'.format(json))
#     utils.data_log(divider=True)

#     if not 'token' in json.keys():

#         response = {}
#         response['status'] = 'Failed'
#         response['alert'] = 'Invalid data!'
#         emit('my response', response, room=clients[0])

#     if json['token'] == '269c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ec':

#         response = {}
#         response['status'] = 'ok'
#         response['new_token'] = '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed'
#         emit('my response', response, room=clients[0])
