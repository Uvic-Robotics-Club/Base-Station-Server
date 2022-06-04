import json
from singleton import Singleton
from threading import Lock

SETTINGS_FILE = 'settings.json'

class Settings(metaclass=Singleton):
    '''
    This thread-safe class stores and modifies the base station server settings during 
    the application lifecycle. The main difference between this class and the State
    class is that the settings values will persist even when the application ends and 
    the server is restarted. A file, SETTINGS_FILE, is used to store base station server
    settings. This inherits the Singleton metaclass, and as such the same settings may 
    be accessed from anywhere inside this application.
    '''
    __lock = Lock()
    __settings = {}

    def __init__(self):
        '''
        Initializes the singleton instance of this class. Opens SETTINGS_FILE and loads
        all values as a dictionary in the class.
        '''
        with open(SETTINGS_FILE) as f:
            self.__settings = json.load(f)

    def set_setting(self, setting_name, value):
        '''
        Sets new value for a setting name. Updates internal class value,
        and also updates settings file so changes persist after program
        termination.
        '''
        assert type(setting_name) == str

        # Acquire lock
        self.__lock.acquire()

        # Change setting and also write to the settings file
        self.__settings[setting_name] = value
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.__settings, f, indent=4, sort_keys=True)

        # Release lock
        self.__lock.release()

    def get_setting(self, setting_name):
        '''
        Returns value of setting_name, if it exists. Raises KeyError if setting value is
        not found.
        '''
        assert type(setting_name) == str
        return self.__settings[setting_name]

    def get_all_settings(self):
        '''
        Returns all settings values.
        '''
        return self.__settings