# pylint: disable=wrong-import-position, import-error, unused-import
""" APP """
from flask import request
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

APP = Flask(__name__, template_folder='ui')
CORS(APP)

SOCKETIO = SocketIO(APP, cors_allowed_origins="*")

# CONNECTION EVENTS
from events.connection import connection

# AUTH EVENTS
from events.auth import auth

# MESSAGE EVENTS
from events.message import message


@APP.route('/')
def home():
    """ HTML """
    return render_template('chat_ui.html')

@APP.route('/all-chat')
def home():
    """ HTML """
    return render_template('all_chat.html')

if __name__ == '__main__':
    SOCKETIO.run(APP, host='0.0.0.0', port=5000)
