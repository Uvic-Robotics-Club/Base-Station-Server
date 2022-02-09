# This file contains methods to send network requests to the rover from the base station.
import requests

def ping(remote_addr, timeout_sec):
    '''
    Sends a GET HTTP request to the remote address specified. If response has 
    status code 200 (OK), returns success.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    try:
        response = requests.get(remote_addr, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        return False, 'Timeout'
    except AssertionError as err:
        return False, 'Status code: {}'.format(response.status_code)

    return True, 'Remote address alive.'

def request_connection(remote_addr, timeout_sec):
    '''
    Sends GET request to request for rover to connect to base station.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    try:
        request_url = '{}/request_connection'.format(remote_addr)
        response = requests.get(request_url, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        return False, 'Timeout'
    except AssertionError as err:
        return False, 'Status code: {}'.format(response.status_code)

    return True, 'Remote address successfully received command.'

def send_command(remote_addr, command, timeout_sec):
    '''
    Sends a POST HTTP request to the remote address with a command to be processed
    by the rover. The command is a dictionary that is sent as JSON MIME Type.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(command) == dict, 'Command must be of type dict.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    # Validate that "type" key in command is specified.
    assert 'type' in command, 'Command must contain "type" key'
    assert type(command['type']) == str, 'Command type must be str type.'

    try:
        request_url = '{}/send_command'.format(remote_addr)
        response = requests.post(request_url, json=command, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        return False, 'Timeout'
    except AssertionError as err:
        return False, 'Status code: {}'.format(response.status_code)

    return True, 'Remote address successfully received command.'