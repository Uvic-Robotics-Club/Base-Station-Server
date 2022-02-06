# This blueprint contains routes which are called by the rover. These routes are not intended to be called by any other
# entities such as the UI.
# NOTE: Currently HTTP connection allows any hosts to pretend to be rover. Converting to
# HTTPS and implement a secret key will minimize chances of threat actor.
from flask import Blueprint, request
from state import State


bp = Blueprint('rover', __name__, url_prefix='/rover')
state = State()

@bp.route('/connect', methods=['GET'])
def connect():
    '''
    Establishes a connection to the server. The 'connection' is an abstraction on top
    of the HTTP requests, which allows the base station to be aware of the history of HTTP
    requests and who is sending/receiving requests.
    '''
    response = {'status': None}

    remote_addr = request.remote_addr

    

    print('Remote address: {}'.format(remote_addr))
    return response