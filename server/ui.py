from flask import Blueprint, request, Response, render_template, stream_with_context
import json
from state import State

bp = Blueprint('ui', __name__, url_prefix='/ui')
state = State()

@bp.route('/', methods=['GET'])
def index():
    '''
    The home page of the application which is the main dashboard 
    of the base station.
    '''
    return render_template('index.html')

@bp.route('/get_connection_status', methods=['GET'])
def get_connection_status():
    '''
    Returns up-to-date connection status by streaming connection
    state.
    '''

    status = {
        'connection_established': state.get_attribute('connection_established'),
        'connection_remote_addr': state.get_attribute('connection_remote_addr'),
        'connection_port': state.get_attribute('connection_port'),
        'connection_id': state.get_attribute('connection_id')
    }
    return status