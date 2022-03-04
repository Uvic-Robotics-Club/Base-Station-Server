# This file contains methods to send network requests to the rover from the base station.
from exceptions import NoConnectionException
from health import HealthCheck
import requests
from random import randrange
from settings import Settings
from state import State
import threading

REQUEST_TIMEOUT_SEC = 5.0

state = State()
settings = Settings()

def connect(remote_addr, port):
    '''
    Sends GET request to request for rover to connect to base station.
    '''
    assert type(remote_addr) == str, 'Remote address must be of type string.'
    assert type(port) == int, 'Port must be of type int.'

    # Generate new connection ID to indicate new connection.
    new_connection_id = randrange(100000000, 999999999)

    try:
        params = {'conn_id': new_connection_id}
        request_url = 'http://{}:{}/connect'.format(remote_addr, port)
        response = requests.get(request_url, params=params, timeout=REQUEST_TIMEOUT_SEC)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as err:
        raise err
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    # Generate new connection ID to indicate new connection.
    new_connection_id = randrange(100000000, 999999999)
    state.set_attribute('connection_id', new_connection_id)
    state.set_attribute('connection_remote_addr', remote_addr)
    state.set_attribute('connection_port', port)
    state.set_attribute('connection_established', True)

    # Start new thread to monitor connection health.
    thread_health_check = threading.Thread(target=HealthCheck.monitor_connection, args=(ping, disconnect))
    thread_health_check.start()

    return response

def send_command(command):
    '''
    Sends a POST HTTP request to the remote address with a command to be processed
    by the rover. The command is a dictionary that is sent as JSON MIME Type.
    '''
    assert type(command) == dict, 'Command must be of type dict.'

    # Validate that "type" key in command is specified.
    assert 'type' in command, 'Command must contain "type" key'
    assert type(command['type']) == str, 'Command type must be str type.'

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        raise NoConnectionException

    try:
        remote_addr = state.get_attribute('connection_remote_addr')
        port = settings.get_setting('port_rover_http')
        request_url = 'http://{}:{}/send_command'.format(remote_addr, port)
        response = requests.post(request_url, json=command, timeout=REQUEST_TIMEOUT_SEC)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as err:
        raise err
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response

def get_telemetry():
    '''
    Sends a GET HTTP request to the rover to fetch the latest telemetry.
    '''

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        raise NoConnectionException

    try:
        remote_addr = state.get_attribute('connection_remote_addr')
        port = settings.get_setting('port_rover_http')
        request_url = 'http://{}:{}/get_rover_telemetry'.format(remote_addr, port)
        response = requests.get(request_url, timeout=REQUEST_TIMEOUT_SEC)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as err:
        raise err
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response

def ping():
    '''
    Sends a GET HTTP request to the remote address specified. If response has 
    status code 200 (OK), returns success.
    '''

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        raise NoConnectionException

    try:
        remote_addr = state.get_attribute('connection_remote_addr')
        port = settings.get_setting('port_rover_http')
        response = requests.get('http://{}:{}'.format(remote_addr, port), timeout=REQUEST_TIMEOUT_SEC)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as err:
        raise err
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response

def disconnect():
    '''
    Sends a GET HTTP request to the remote address indicating that the base station
    is disconnecting from the rover. The rover will simply accept the disconnect request
    and not send back another request past the response.
    '''

    # If no connection exists, return failure.
    if not state.get_attribute('connection_established'):
        raise NoConnectionException

    # Set state variables
    state.set_attribute('connection_id', None)
    state.set_attribute('connection_remote_addr', None)
    state.set_attribute('connection_port', None)
    state.set_attribute('connection_established', False)

    try:
        remote_addr = state.get_attribute('connection_remote_addr')
        port = settings.get_setting('port_rover_http')
        request_url = 'http://{}:{}/disconnect'.format(remote_addr, port)
        response = requests.get(request_url, timeout=REQUEST_TIMEOUT_SEC)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as err:
        raise err
    except requests.exceptions.Timeout as ex:
        raise ex
    except AssertionError as err:
        raise err

    return response