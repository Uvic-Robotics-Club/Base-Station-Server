import json
from state import Singleton
from threading import Lock

SETTINGS_FILE = 'settings.json'

class Settings(metaclass=Singleton):
    __lock = Lock()
    __settings = {}

    def __init__(self):
        # Load settings stored in file when instantiating class
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
        assert type(setting_name) == str
        return self.__settings[setting_name]

    def get_all_settings(self):
        return self.__settings