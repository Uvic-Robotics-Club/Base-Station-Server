# This blueprint contains routes which are called by the UI. Routes include returning the current state, 
# sending commands to the rover, and so on...
#from client import send_command, connect, disconnect
import client
from flask import Blueprint, request
import requests
from settings import Settings
from state import State


bp = Blueprint('ui', __name__, url_prefix='/ui')
state = State()
settings = Settings()

@bp.route('/connect_rover', methods=['GET'])
def connect_rover():
    '''
    Sends HTTP request to specified remote address to connect to
    base station.
    '''
    response = {'status': None}
    args = dict(request.args)

    # Validate remote adress parameter is present.
    try:
        assert 'remote_addr' in args, 'remote_addr parameter not provided.'
    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    # If connection already exists, fail.
    # TODO: Determine if this is appropriate
    #if state.get_attribute('connection_established'):
    #    response['status'] = 'failure'
    #    response['message'] = 'Established connection exists. Disconnect first, then reconnect.'

    try:
        rover_response = client.connect(
            remote_addr = args['remote_addr'],
            port = settings.get_setting('port_rover_http'),
            timeout_sec = settings.get_setting('timeout_request_connection_sec')
        )
    except requests.exceptions.Timeout as ex:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError as err:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response
    
    return rover_response.json()

@bp.route('/send_command', methods=['GET', 'POST'])
def send_command():
    '''
    Sends command to the rover, if a connection exists. Command must be of
    JSON data type of a recognized format.
    '''
    response = {'status': None}

    if request.method == 'POST' and (not request.is_json):
        response['status'] = 'failure'
        response['message'] = 'Request\'s MIME type is not application/json.'
        return response

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to send command.'
        return response

    # Validate command JSON
    # NOTE: Handles GET for testing
    if request.method == 'POST':
        json_data = request.get_json()
    else:
        json_data = dict(request.args)

    try:
        # Send command
        result = client.send_command(
            remote_addr = state.get_attribute('connection_remote_addr'), 
            port = settings.get_setting('port_rover_http'),
            command = json_data,
            timeout_sec = settings.get_setting('timeout_send_command_sec')
            )
    except requests.exceptions.Timeout as ex:
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

@bp.route('/disconnect_rover', methods=['GET'])
def disconnect_rover():
    '''
    Disconnects base station from rover, if a connection exists.
    '''
    response = {'status': None}

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, no connections to disconnect.'
        return response

    try:
        # Send request to rover
        result = client.disconnect(
            remote_addr = state.get_attribute('connection_remote_addr'), 
            port = settings.get_setting('port_rover_http'),
            timeout_sec = settings.get_setting('timeout_send_command_sec')
        )
    except requests.exceptions.Timeout as ex:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError as err:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response

    # Set state variables
    state.set_attribute('connection_id', None)
    state.set_attribute('connection_remote_addr', None)
    state.set_attribute('connection_established', False)

    response['status'] = 'success'
    response['message'] = 'Successfully disconnected from rover.'
    return response

@bp.route('/force_disconnect_rover', methods=['GET'])
def force_disconnect_rover():
    '''
    Terminates connection to rover from base station without waiting for
    response from rover. This would mainly be used if the rover cannot be 
    reached
    '''
    response = {'status': None}

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection, no connections to disconnect.'
        return response 

    try:
        # Send request to rover, with short timeout. Ideally, would send
        # async request, but requests module does not have support currently.
        client.disconnect(
            remote_addr = state.get_attribute('connection_remote_addr'), 
            port = settings.get_setting('port_rover_http'),
            timeout_sec = 0.1 # 0.1 second timeout
        )
    except requests.exceptions.Timeout as ex:
        pass

    # Set state variables
    state.set_attribute('connection_id', None)
    state.set_attribute('connection_remote_addr', None)
    state.set_attribute('connection_established', False)

    response['status'] = 'success'
    response['message'] = 'Successfuly forcefully closed connection.'
    return response


@bp.route('/scan_ip_addresses', methods=['GET'])
def scan_ip_addresses():
    '''
    Scans the local network IP addresses.
    '''
    response = {'status': None}
    return response

