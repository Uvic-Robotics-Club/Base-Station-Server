# This file contains methods to send network requests to the rover from the base station.
import requests
from random import randrange
from state import State

state = State()

def ping(remote_addr, port, timeout_sec):
    '''
    Sends a GET HTTP request to the remote address specified. If response has 
    status code 200 (OK), returns success.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(port) == int, 'Port must be of type int.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    try:
        response = requests.get('http://{}:{}'.format(remote_addr, port), timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        return False, 'Timeout'
    except AssertionError as err:
        return False, 'Status code: {}'.format(response.status_code)

    return True, 'Remote address alive.'

def connect(remote_addr, port, timeout_sec):
    '''
    Sends GET request to request for rover to connect to base station.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(port) == int, 'Port must be of type int.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    # Generate new connection ID to indicate new connection.
    new_connection_id = randrange(100000000, 999999999)

    try:
        params = {'conn_id': new_connection_id}
        request_url = 'http://{}:{}/connect'.format(remote_addr, port)
        response = requests.get(request_url, params=params, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    # Generate new connection ID to indicate new connection.
    new_connection_id = randrange(100000000, 999999999)
    state.set_attribute('connection_id', new_connection_id)
    state.set_attribute('connection_remote_addr', remote_addr)
    state.set_attribute('connection_established', True)

    return response

def send_command(remote_addr, port, command, timeout_sec):
    '''
    Sends a POST HTTP request to the remote address with a command to be processed
    by the rover. The command is a dictionary that is sent as JSON MIME Type.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(port) == int, 'Port must be of type int.'
    assert type(command) == dict, 'Command must be of type dict.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    # Validate that "type" key in command is specified.
    assert 'type' in command, 'Command must contain "type" key'
    assert type(command['type']) == str, 'Command type must be str type.'

    try:
        request_url = 'http://{}:{}/send_command'.format(remote_addr, port)
        response = requests.post(request_url, json=command, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response

def disconnect(remote_addr, port, timeout_sec):
    '''
    Sends a GET HTTP request to the remote address indicating that the base station
    is disconnecting from the rover. The rover will simply accept the disconnect request
    and not send back another request past the response.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(port) == int, 'Port must be of type int.'
    assert type(timeout_sec) in [int, float], 'Timeout must be of type int or float.'

    try:
        request_url = 'http://{}:{}/disconnect'.format(remote_addr, port)
        response = requests.get(request_url, timeout=timeout_sec)
        assert response.status_code == 200
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response