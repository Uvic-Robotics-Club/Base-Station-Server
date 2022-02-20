# This blueprint contains routes which are called by the UI. Routes include returning the current state, 
# sending commands to the rover, and so on...
from client import send_command, send_connection_request, disconnect
from flask import Blueprint, request
import requests
from settings import Settings
from state import State


bp = Blueprint('ui', __name__, url_prefix='/ui')
state = State()
settings = Settings()

@bp.route('/request_connection', methods=['GET'])
def request_connection():
    '''
    Sends HTTP request to specified remote address to request for it 
    to connect to the base station.
    '''
    response = {'status': None}
    args = dict(request.args)

    # Validate remote adress parameter is present.
    try:
        assert 'remote_addr' in args, 'remote_attr parameter not provided.'
    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    # If connection already exists, fail.
    if state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'Established connection exists. Disconnect first, then reconnect.'

    try:
        rover_response = send_connection_request(
            remote_addr = args['remote_addr'],
            port = settings.get_setting('port_rover_http'),
            timeout_sec = settings.get_setting('timeout_request_connection_sec')
        )
    except requests.exception.Timeout as ex:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError as err:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response
    
    return rover_response.json()

@bp.route('/send_command', methods=['POST'])
def send_command():
    '''
    Sends command to the rover, if a connection exists. Command must be of
    JSON data type of a recognized format.
    '''
    response = {'status': None}

    if not request.is_json:
        response['status'] = 'failure'
        response['message'] = 'Request\'s MIME type is not application/json.'
        return response

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to send command.'
        return response

    # Validate command JSON
    json_data = request.get_json()

    try:
        # Send command
        result = send_command(
            remote_addr = state.get_attribute('connection_remote_addr'), 
            command = json_data,
            timeout_sec = settings.get_setting('timeout_send_command_sec')
            )
    except requests.exception.Timeout as ex:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError as err:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response

    return result.json()

@bp.route('/get_rover_telemetry', methods=['GET'])
def get_rover_telemetry():
    '''
    Gets telemetry from the rover, if a connection exists.
    '''
    response = {'status': None}

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to send command.'
        return response

    telemetry_data = state.get_attribute('rover_telemetry')
    response['status'] = 'success'
    response['data'] = telemetry_data
    return response

@bp.route('/disconnect', methods=['GET'])
def disconnect():
    '''
    Disconnects base station from rover, if a connection exists.
    '''
    response = {'status': None}

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, no connections to disconnect.'
        return response        

    result = disconnect(
        remote_addr = state.get_attribute('connection_remote_addr'), 
        port = state.get_attribute('port_rover_http'),
        timeout_sec = settings.get_setting('timeout_send_command_sec')
    )

@bp.route('/scan_ip_addresses', methods=['GET'])
def scan_ip_addresses():
    '''
    Scans the local network IP addresses.
    '''
    response = {'status': None}
    return response

