from flask import Blueprint, request
from state import State
import subprocess
from .utils import assert_expected_keys_list, get_header_key_indexes

bp = Blueprint('api/hotspot', __name__, url_prefix='/api/hotspot')
state = State()

@bp.route('/get_network_interfaces', methods=['GET'])
def get_network_interfaces():
    '''
    Returns a list of the device's network interfaces, along with their status.
    '''
    # TEST URL: http://127.0.0.1:5000/hotspot/get_network_interfaces
    response = {'status': None}

    try:
        unparsed_output_by_line = str(subprocess.check_output('nmcli device status', stderr=subprocess.STDOUT, shell=True))[2:].split('\\n')[:-1]
    except subprocess.CalledProcessError as err:
        response['status'] = 'OS command exited with non-zero code'
        response['message'] = 'Return code: {}, Output: {}'.format(err.returncode, err.output)
        return response

    headers = unparsed_output_by_line[0]
    headers_keys = headers.split()

    # Assert header keys are expected output, and get key indexes to allow for correct parsing
    assert_expected_keys_list(headers_keys, 4, ['DEVICE', 'TYPE', 'STATE', 'CONNECTION'])
    headers_key_indexes = get_header_key_indexes(headers, ['DEVICE', 'TYPE', 'STATE', 'CONNECTION'])

    network_interfaces_list = []
    for line in unparsed_output_by_line[1:]:
        # Append network interface details to list
        network_interfaces_list.append({
            'DEVICE': line[headers_key_indexes['DEVICE']: headers_key_indexes['TYPE']].strip(),
            'TYPE': line[headers_key_indexes['TYPE']: headers_key_indexes['STATE']].strip(),
            'STATE': line[headers_key_indexes['STATE']: headers_key_indexes['CONNECTION']].strip(),
            'CONNECTION': line[headers_key_indexes['CONNECTION']:].strip()
        })

    response['status'] = 'success'
    response['output'] = network_interfaces_list
    return response

@bp.route('/get_current_active_connections', methods=['GET'])
def get_current_active_connections():
    '''
    '''
    # TEST URL: http://127.0.0.1:5000/hotspot/get_current_active_connections 
    response = {'status': None}

    try:
        unparsed_output_by_line = str(subprocess.check_output('nmcli connection show --active', stderr=subprocess.STDOUT, shell=True))[2:].split('\\n')[:-1]
    except subprocess.CalledProcessError as err:
        response['status'] = 'OS command exited with non-zero code'
        response['message'] = 'Return code: {}, Output: {}'.format(err.returncode, err.output)
        return response

    # Get headers. If no headers are present, this means no connections currently active, and return empty list.
    headers = unparsed_output_by_line[0]
    if len(headers) == 0:
        response['status'] = 'success'
        response['output'] = []
        return response

    headers_keys = headers.split()

    # Assert header keys are expected output, and get key indexes to allow for correct parsing
    assert_expected_keys_list(headers_keys, 4, ['NAME', 'UUID', 'TYPE', 'DEVICE'])
    headers_key_indexes = get_header_key_indexes(headers, ['NAME', 'UUID', 'TYPE', 'DEVICE'])

    current_active_connections_list = []
    for line in unparsed_output_by_line[1:]:
        # Append each connection detail. Each value is parsed by getting substring corresponding to key indexes as delimiters
        current_active_connections_list.append({
            'NAME': line[headers_key_indexes['NAME']: headers_key_indexes['UUID']].strip(),
            'UUID': line[headers_key_indexes['UUID']: headers_key_indexes['TYPE']].strip(),
            'TYPE': line[headers_key_indexes['TYPE']: headers_key_indexes['DEVICE']].strip(),
            'DEVICE': line[headers_key_indexes['DEVICE']:].strip()
        })

    response['status'] = 'success'
    response['output'] = current_active_connections_list
    return response

@bp.route('/status', methods=['GET'])
def status():
    '''
    Returns the status of the WiFi hotspot.
    '''
    response = {'status': None}

    # Assert WiFi hotspot is on before disconnecting
    active_connections = get_current_active_connections()['output']
    hotspot_active = False
    hotspot_device = None
    for connection in active_connections:
        if connection['NAME'] == 'Hotspot':
            hotspot_active = True
            hotspot_device = connection['DEVICE']

    # Update state as soon as most recent knowledge of hotspot available.
    state.set_attribute('hotspot_active', hotspot_active)
    if not hotspot_active:
        response['status'] = 'success'
        response['hotspot_active'] = False
        return response

    response['status'] = 'success'
    response['hotspot_active'] = True
    response['device'] = hotspot_device
    return response

@bp.route('/start', methods=['GET'])
def start():
    '''
    Starts WiFi hotspot

    Request parameters:
        ifname: WiFi device to be used
        # conname: Name of created hotspot connection profile
        ssid: Hotspot SSID
        # band: WiFi band to use
        # channel: WiFi channel to use
        password: Password to use for created hotspot

    '''
    # TEST URL: http://127.0.0.1:5000/hotspot/start?ifname=wlp7s0&ssid=test&password=test1234

    response = {'status': None}
    args = dict(request.args)

    # Validate all required request parameters are present
    try:
        assert 'ifname' in args, 'ifname parameter not provided.'
        #assert 'conname' in args, 'conname parameter not provided.'
        assert 'ssid' in args, 'ssid parameter not provided.'
        #assert 'band' in args, 'band parameter not provided.'
        #assert 'channel' in args, 'channel parameter not provided.'
        assert 'password' in args, 'password parameter not provided.'

    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    # If connection already exists, then fail.
    if status()['hotspot_active']:
        response['status'] = 'failure'
        response['message'] = 'Cannot start new hotspot, another hotspot is active.'
        return response

    try:
        command_to_execute = 'nmcli dev wifi hotspot ifname {} ssid {} password "{}"'
        output = str(subprocess.check_output(command_to_execute.format(args['ifname'], args['ssid'], args['password']), stderr=subprocess.STDOUT, shell=True))[11:].split('\\n')[0]
        
        state.set_attribute('hotspot_active', True)
    except subprocess.CalledProcessError as err:
        response['status'] = 'OS command exited with non-zero code'
        response['message'] = 'Return code: {}, Output: {}'.format(err.returncode, err.output)
        return response

    response['status'] = 'success'
    response['message'] = output
    return response

@bp.route('/stop', methods=['GET'])
def stop():
    '''
    Stops WiFi hotspot

    Request parameters:
    '''
    response = {'status': None}

    # Assert WiFi hotspot is on before disconnecting
    hotspot_status = status()
    is_hotspot_active = hotspot_status['hotspot_active']
    if not is_hotspot_active:
        response['status'] = 'No active hotspots found.'
        return response

    # Disconnect hotspot.
    try:
        output = str(subprocess.check_output('nmcli device disconnect {}'.format(hotspot_status['device']), stderr=subprocess.STDOUT, shell=True))[2:]
        state.set_attribute('hotspot_active', False)
    except subprocess.CalledProcessError as err:
        response['status'] = 'OS command to stop hotspot'
        response['message'] = 'Return code: {}, Output: {}'.format(err.returncode, err.output)
        return response

    response['status'] = 'success'
    response['message'] = output
    return response