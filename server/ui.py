from flask import Blueprint, render_template, request
from settings import Settings
from state import State
from time import sleep

bp = Blueprint('ui', __name__, url_prefix='/ui')
settings = Settings()
state = State()

@bp.route('/', methods=['GET'])
def index():
    '''
    The home page of the application which is the main dashboard 
    of the base station.
    '''
    return render_template('index.html')

@bp.route('/settings', methods=['GET'])
def settings_page():
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

@bp.route('/get_settings', methods=['GET'])
def get_settings():
    '''
    Returns base station settings.
    '''
    settings_json = settings.get_all_settings()
    return settings_json

@bp.route('/change_settings', methods=['GET'])
def change_settings():
    '''
    Changes a base station settings.
    '''
    response = {'status': None}
    args = dict(request.args)

    # If no settings are provided, fail
    try:
        assert len(args) > 0
    except AssertionError:
        response['status'] = 'failure'
        response['message'] = 'No settings are provided to be changed.'
        return response

    # Set setting values for each parameter
    for setting_name in args:
        setting_value = args[setting_name]
        settings.set_setting(setting_name, setting_value)

    response['status'] = 'success'
    response['message'] = 'Successfully changed settings'
    return response

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