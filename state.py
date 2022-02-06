'''
Thread-safe implementation of a collection of states that must be stored when the server
is active. The collection is a singleton class, and so there is only one instance of this 
class that can exist at one time.
'''
from threading import Lock

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class State(metaclass=Singleton):
    __lock_set_attr = Lock()
    __data = {}

    def __init__(self):
        # Initialize default data
        pass
    
    def set_attribute(self, attribute_name, value):
        assert type(attribute_name) == str

        # Acquire lock
        self.__lock_set_attr.acquire()
        self.__data[attribute_name] = value
        # Release lock
        self.__lock_set_attr.release()

    def get_attribute(self, attribute_name):
        assert type(attribute_name) == str
        return self.__data[attribute_name]

    def delete_attribute(self, attribute_name):
        assert type(attribute_name) == str

        # Acquire lock
        self.__lock_set_attr.acquire()
        del self.__data[attribute_name]
        # Release lock
        self.__lock_set_attr.release()