
class Singleton(type):
    '''
    This metaclass restricts the instantiation of a class to one object. It is a type
    of creational pattern and involves only one class to create methods and specified
    objects. Once a class inheriting the `Singleton` class is initialized, only one
    instance of that class shall exist in memory. This ensures that multiple threads 
    using the same class will not instantiate more tahn one instance at a time.
    Furthermore it allows for data to be shared across the application.
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]