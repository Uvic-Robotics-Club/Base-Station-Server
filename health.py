'''
This file contains code which is reponsible for ensuring that the connection
to the rover is still alive.
'''
import exceptions
import requests
from settings import Settings
from state import State
from time import sleep, time

state = State()
settings = Settings()

class HealthCheck():

    @staticmethod
    def monitor_connection(ping, disconnect):
        '''
        Monitors current connection, if any, as part of health
        checks.
        '''
        assert callable(ping)
        assert callable(disconnect)

        if not state.get_attribute('connection_established'):
            return
        connection_id = state.get_attribute('connection_id')

        last_response_timestamp = float('inf')
        while (time() - last_response_timestamp) < float(settings.get_setting('healthcheck_timeout_rover_connection_sec')):
            
            # Wait for ping interval, then ping rover.
            sleep(float(settings.get_setting('healthcheck_interval_rover_ping_sec')))

            # If connection ID is different, then return.
            if connection_id != state.get_attribute('connection_id'):
                state.set_attribute('connection_ping_status', None)
                state.set_attribute('connection_ping_last_response', None)
                
                print('Health check: Connection ID has changed, ending health check thread.')
                return

            # If connection is now closed, then return.
            if not state.get_attribute('connection_established'):
                state.set_attribute('connection_ping_status', None)
                state.set_attribute('connection_ping_last_response', None)
                
                print('Health check: Connection closed by another thread.')
                return

            try:
                ping()
                state.set_attribute('connection_ping_status', 'healthy')
                state.set_attribute('connection_ping_last_response', time())
                last_response_timestamp = time()

                print('Health check: Ping success!')
            except requests.exceptions.ConnectionError as err:
                state.set_attribute('connection_ping_status', 'unreachable')
            except requests.exceptions.Timeout as ex:
                state.set_attribute('connection_ping_status', 'unreachable')
            except AssertionError as err:
                state.set_attribute('connection_ping_status', 'unreachable')

        # Forcibly disconnect from the rover.
        try:
            # Send request to rover, with short timeout. Ideally, would send
            # async request, but requests module does not have support currently.
            state.set_attribute('connection_ping_status', 'timeout')
            print('Timeout, disconnecting from rover.')
            disconnect()
        except exceptions.NoConnectionException:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except AssertionError:
            pass

        # Reset ping state parameters
        state.set_attribute('connection_ping_status', None)
        state.set_attribute('connection_ping_last_response', None)
