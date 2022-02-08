# This blueprint contains routes which are called by the UI. Routes include returning the current state, 
# sending commands to the rover, and so on...
from client import send_command
from flask import Blueprint, request
from settings import Settings
from state import State


bp = Blueprint('ui', __name__, url_prefix='/ui')
state = State()
settings = Settings()

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

    # Send command
    result = send_command(
        remote_addr = state.get_attribute('connection_remote_addr'), 
        command = json_data,
        timeout_sec = settings.get_setting('timeout_send_command_sec')
        )

    # TODO: Complete

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


@bp.route('/scan_ip_addresses', methods=['GET'])
def scan_ip_addresses():
    '''
    Scans the local network IP addresses.
    '''
    response = {'status': None}
    # TODO

