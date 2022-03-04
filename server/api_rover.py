# This blueprint contains routes which are called by the UI. Routes include returning the current state, 
# sending commands to the rover, and so on...
import client
import exceptions
from flask import Blueprint, request
import requests
from settings import Settings
from state import State


bp = Blueprint('api/rover', __name__, url_prefix='/api/rover')
state = State()
settings = Settings()

@bp.route('/connect', methods=['GET'])
def connect():
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

    try:
        rover_response = client.connect(
            remote_addr = args['remote_addr'],
            port = settings.get_setting('port_rover_http')
        )
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to ping rover server.'
        return response
    except requests.exceptions.ConnectionError as err:
        response['status'] = 'failure'
        response['message'] = 'ConnectionError: Max retries exceeded with URL.'
        return response
    except requests.exceptions.Timeout:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError:
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

    # Validate command JSON
    # NOTE: Handles GET for testing
    if request.method == 'POST':
        json_data = request.get_json()
    else:
        json_data = dict(request.args)

    try:
        # Send command
        response = client.send_command(command = json_data)
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to ping rover server.'
        return response
    except requests.exceptions.ConnectionError as err:
        response['status'] = 'failure'
        response['message'] = 'ConnectionError: Max retries exceeded with URL.'
        return response
    except requests.exceptions.Timeout:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response
        
    return response.json()

@bp.route('/get_telemetry', methods=['GET'])
def get_telemetry():
    '''
    Gets telemetry from the rover, if a connection exists.
    '''
    response = {'status': None}

    try:
        rover_response = client.get_telemetry()
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to ping rover server.'
        return response
    except requests.exceptions.ConnectionError as err:
        response['status'] = 'failure'
        response['message'] = 'ConnectionError: Max retries exceeded with URL.'
        return response
    except requests.exceptions.Timeout:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response
    
    return rover_response.json()

@bp.route('/ping', methods=['GET'])
def ping():
    '''
    Pings the rover to ensure that it is alive.
    '''
    response = {'status': None}

    try:
        response = client.ping()
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, unable to ping rover server.'
        return response
    except requests.exceptions.ConnectionError as err:
        response['status'] = 'failure'
        response['message'] = 'ConnectionError: Max retries exceeded with URL.'
        return response
    except requests.exceptions.Timeout:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response
    
    return response.json()

@bp.route('/disconnect', methods=['GET'])
def disconnect():
    '''
    Disconnects base station from rover, if a connection exists.
    '''
    response = {'status': None}

    try:
        # Send request to rover
        response = client.disconnect()
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, no connection to disconnect.'
        return response
    except requests.exceptions.ConnectionError as err:
        response['status'] = 'failure'
        response['message'] = 'ConnectionError: Max retries exceeded with URL.'
        return response
    except requests.exceptions.Timeout:
        response['status'] = 'failure'
        response['message'] = 'Request to rover timed out.'
        return response
    except AssertionError:
        response['status'] = 'failure'
        response['message'] = 'Response status code is not 200 OK.'
        return response

    return response.json()

@bp.route('/force_disconnect', methods=['GET'])
def force_disconnect():
    '''
    Terminates connection to rover from base station without waiting for
    response from rover. This would mainly be used if the rover cannot be 
    reached
    '''
    response = {'status': None}

    try:
        # Send request to rover. Ideally, would send async request, but requests 
        # module does not have that support currently.
        client.disconnect()
    except exceptions.NoConnectionException:
        response['status'] = 'failure'
        response['message'] = 'No established connection, no connections to disconnect.'
        return response 
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    except AssertionError:
        pass

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

