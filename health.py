'''
This file contains code which is reponsible for ensuring that the connection
to the rover is still alive.
'''
import exceptions
import requests
from settings import Settings
from state import State
from time import sleep, time

# Initializes health check thread. If a connection exists, 
# keep checking 

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

        last_response_timestamp = float('inf')
        while (time() - last_response_timestamp) < settings.get_setting('healthcheck_timeout_rover_connection_sec'):
            
            # Wait for ping interval, then ping rover.
            sleep(settings.get_setting('healthcheck_interval_rover_ping_sec'))

            # If connection is now closed, then return.
            if not state.get_attribute('connection_established'):
                print('Health check: Connection closed by another thread.')
                return

            try:
                ping()
                print('Health check: Ping success!')
            except requests.exceptions.ConnectionError as err:
                continue
            except requests.exceptions.Timeout as ex:
                continue
            except AssertionError as err:
                continue
            
            last_response_timestamp = time()

        # Forcibly disconnect from the rover.
        try:
            # Send request to rover, with short timeout. Ideally, would send
            # async request, but requests module does not have support currently.
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
