from flask import Blueprint, render_template
from state import State
from time import sleep

bp = Blueprint('ui', __name__, url_prefix='/ui')
state = State()

@bp.route('/', methods=['GET'])
def index():
    '''
    The home page of the application which is the main dashboard 
    of the base station.
    '''
    return render_template('index.html')

@bp.route('/settings', methods=['GET'])
def settings():
    '''
    The settings page of the application which contains configuration
    options for the base station and the rover.
    '''
    return render_template('settings.html')

@bp.route('/get_state', methods=['GET'])
def get_state():
    '''
    Returns up-to-date application state. 
    '''
    state_json = state.get_all_attributes()
    return state_json

@bp.route('/get_state_long_poll', methods=['GET'])
def get_state_long_poll():
    '''
    Returns up-to-date application state by returning request 
    only when state changes.
    '''
    current_state_json = state.get_all_attributes()
    latest_state_json = current_state_json.copy()

    while latest_state_json == current_state_json:
        sleep(0.2)
        latest_state_json = state.get_all_attributes()
    return latest_state_json