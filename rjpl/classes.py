
class Place:
    def __init__(self):
        raise NotImplementedError('This class is abstract.')

class Coord(Place):
    def __init__(self, coordX, coordY, name='Location'):
        if isinstance(coordX, float) and isinstance(coordY, float) and isinstance(name, str):
            self.coordX = coordX
            self.coordY = coordY
            self.name = name
        else:
            raise TypeError("Expected <class 'float'>, <class 'float'>, <class 'str'> got {}, {} and {}.".format(type(coordX), type(coordY), type(name)))


class Stop(Place):
    def __init__(self, stop_id):
        if isinstance(stop_id, int):
            self.stop_id = stop_id
        else:
            raise TypeError("Expected <class 'int'> got {}.".format(type(stop_id)))


class rjplAPIError(Exception):
    """Raised when the API returned an error."""
    pass

class rjplConnectionError(Exception):
    """Raised in the event of a network problem."""
    pass

class rjplHTTPError(Exception):
    """Raised when the HTTP response code is not 200."""
    pass