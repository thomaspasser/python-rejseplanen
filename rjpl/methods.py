"""
Python implementation of communication with Rejseplanen API.

More information about the API can be found at
https://help.rejseplanen.dk/hc/en-us/articles/214174465-Rejseplanen-s-API

"""
from datetime import datetime
import requests

from .classes import *
from .constants import *

def _request(service, params, timeout):
    params['format'] = 'json'
    
    try:
        response = requests.get(RESOURCE+service, params, timeout=timeout)
    except requests.exceptions.RequestException as e:
        raise rjplConnectionError(e)

    if response.status_code == 200:
        return response.json()
    else:
        raise rjplHTTPError('Error: ' + str(response.status_code) +
                str(response.content))

def location(input, timeout=5):
    """ Perform a pattern matching of user input.

    Args:
        input (str): The search input.
        timeout (int): Timeout time of requests.get() call in seconds.

    Returns:
        Dictionary object.
        Keys:
            'StopLocation':  List of dictionaries of stop locations with coordinates.
            'CoordLocation': List of dictionaries of named points of interests with coordinates.
    """
    params = {}

    if isinstance(input, str):
        params['input'] = input
    else:
        raise TypeError("Expected <class 'str'> got {}".format(type(input)))
    
    response = _request('location', params, timeout)

    result = response['LocationList']

    if 'error' in result:
        raise rjplAPIError(result['error'])

    return result

def trip(origin, destination, viaId=None, time=None, searchForArrival=None, useTrain=True, 
         useBus=True, useMetro=True, useBicycle=False, maxWalkingDistanceDep=None, 
         maxWalkingDistanceDest=None, maxCyclingDistanceDep=None, maxCyclingDistanceDest=None, timeout=10):
    """ Calculates trip from specified origin to specified destination. 

    Args:
        origin (rjpl.Coord or rjpl.Stop): Trip origin.
        destination (rjpl.Coord or rjpl.Stop): Trip destination.
        viaId (int): Id of stop to force the trip through.
        time (datetime): Departure date and time of the trip. (default: current server time)
        searchForArrival (bool): If true, time will be used for arrival time instead. (default: False)
        useTrain (bool): Whether to travel by train (default: True)
        useBus (bool): Whether to travel by bus (default: True)
        useMetro (bool): Whether to travel by metro (default: True)
        useBicycle (bool): Restrict to trips which allow carriage of bicycles. (default: False)
        timeout (int): Timeout time of requests.get() call in seconds.

    Extra args if useBicycle=False:
        maxWalkingDistanceDep (int): The max walking distance from start location to the first mode of transportation.
        maxWalkingDistanceDest (int): The max walking distance from last mode of transportation to the destination.

    Extra args if useBicycle=True
        maxCyclingDistanceDep (int): The max biking distance from start location to the first mode of public transportation.
        maxCyclingDistanceDest (int): The max biking distance from the last mode of public transportation to the destination.

    Returns:
        List of possible trips from origin to destination. The trips are given as dictonaries, with a list of legs.
    """
    params = {}

    if isinstance(origin, Place):
        if isinstance(origin, Stop):
            params['originId'] = origin.stop_id
        elif isinstance(origin, Coord):
            params['originCoordX'] = int(COORDINATE_MULTIPLIER*origin.coordX)
            params['originCoordY'] = int(COORDINATE_MULTIPLIER*origin.coordY)
            params['originCoordName'] = origin.name
        else:
            raise TypeError("Unknown instance of <class 'Place'>.")
    else:
        raise TypeError("Expected <class 'Place'> got {}.".format(type(origin)))

    if isinstance(destination, Place):
        if isinstance(destination, Stop):
            params['destId'] = destination.stop_id
        elif isinstance(destination, Coord):
            params['destCoordX'] = int(COORDINATE_MULTIPLIER*destination.coordX)
            params['destCoordY'] = int(COORDINATE_MULTIPLIER*destination.coordY)
            params['destCoordName'] = destination.name
        else:
            raise TypeError("Unknown instance of <class 'Place'>.")
    else:
        raise TypeError("Expected <class 'Place'> got {}.".format(type(destination)))

    if viaId is not None:
        if isinstance(viaId, int):
            params['viaId'] = viaId
        else:
            raise TypeError("Expected <class 'int'> got {}.".format(type(viaId)))

    if searchForArrival is not None:
        if isinstance(searchForArrival, bool):
            params['searchForArrival'] = int(searchForArrival)
        else:
            raise TypeError("Expected <class 'bool'>, got {}.".format(type(searchForArrival)))
    
    if isinstance(useTrain, bool):
        params['useTog'] = int(useTrain)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useTrain)))
    
    if isinstance(useBus, bool):
        params['useBus'] = int(useBus)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useBus)))
    
    if isinstance(useMetro, bool):
        params['useMetro'] = int(useMetro)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useMetro)))
    
    if time:
        if isinstance(time, datetime):
            params['date'] = time.strftime(DATE_FORMAT)
            params['time'] = time.strftime(TIME_FORMAT)
        else:
            raise TypeError('Expected datetime.datime, got {}.'.format(type(time)))

    if isinstance(useBicycle, bool):
        params['useBicycle'] = int(useBicycle)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useBus)))

    if useBicycle:
        if maxWalkingDistanceDep is not None:
            raise ValueError("Can't use maxWalkingDistanceDep with useBicycle.")
        if maxWalkingDistanceDest is not None:
            raise ValueError("Can't use maxWalkingDistanceDest with useBicycle.")

        if maxCyclingDistanceDep is not None:
            if isinstance(maxCyclingDistanceDep, int):
                if maxCyclingDistanceDep >= 500 and maxCyclingDistanceDep <= 20000:
                    params['maxCyclingDistanceDep'] = maxCyclingDistanceDep
                else:
                    raise ValueError("maxCyclingDistanceDep out of bounds.")
            else:
                raise TypeError("Expected <class 'int'>, got {}.".format(type(maxCyclingDistanceDep)))    
        if maxCyclingDistanceDest is not None:
            if isinstance(maxCyclingDistanceDest, int):
                if maxCyclingDistanceDest >= 500 and maxCyclingDistanceDest <= 20000:
                    params['maxCyclingDistanceDest'] = maxCyclingDistanceDest
                else:
                    raise ValueError("maxCyclingDistanceDest out of bounds.")
            else:
                raise TypeError("Expected <class 'int'>, got {}.".format(type(maxCyclingDistanceDest)))

    else:
        if maxCyclingDistanceDep is not None:
            raise ValueError("Can't use maxCyclingDistanceDep without useBicycle.")
        if maxCyclingDistanceDest is not None:
            raise ValueError("Can't use maxCyclingDistanceDest without useBicycle.")

        if maxWalkingDistanceDep is not None:
            if isinstance(maxWalkingDistanceDep, int):
                if maxWalkingDistanceDep >= 500 and maxWalkingDistanceDep <= 20000:
                    params['maxWalkingDistanceDep'] = maxWalkingDistanceDep
                else:
                    raise ValueError("maxWalkingDistanceDep out of bounds.")
            else:
                raise TypeError("Expected <class 'int'>, got {}.".format(type(maxWalkingDistanceDep)))    
        if maxWalkingDistanceDest is not None:
            if isinstance(maxWalkingDistanceDest, int):
                if maxWalkingDistanceDest >= 500 and maxWalkingDistanceDest <= 20000:
                    params['maxWalkingDistanceDep'] = maxWalkingDistanceDest
                else:
                    raise ValueError("maxWalkingDistanceDest out of bounds.")
            else:
                raise TypeError("Expected <class 'int'>, got {}.".format(type(maxWalkingDistanceDest)))  

    response = _request('trip', params, timeout)

    result = response['TripList']
    if 'error' in result:
        raise rjplAPIError(result['error'])

    return result['Trip']


def departureBoard(stop_id, useTrain=True, useBus=True, useMetro=True, time=None, offset=None, timeout=10):
    """ Retrieve a station departure board.

    Args:
        stop_id (int): The station id. Can be retrieved with the location() call.
        useTrain (bool): Whether to travel by train (default: True)
        useBus (bool): Whether to travel by bus (default: True)
        useMetro (bool): Whether to travel by metro (default: True)
        time (datetime): Departure date and time of the trip. (default: current server time)
        offset (int): Search a number of minutes into the future. Use either time or offset.
        timeout (int): Timeout time of requests.get() call in seconds.

    Returns:
        A list of dictionaries, each containing departure name, time, direction and type.
    """
    params = {}

    if type(stop_id) is int:
        params['id'] = stop_id
    else:
        raise TypeError("Expected <class 'int'>, got {}.".format(type(stop_id)))

    if isinstance(useTrain, bool):
        params['useTog'] = int(useTrain)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useTrain)))
    
    if isinstance(useBus, bool):
        params['useBus'] = int(useBus)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useBus)))
    
    if isinstance(useMetro, bool):
        params['useMetro'] = int(useMetro)
    else:
        raise TypeError("Expected <class 'bool'>, got {}.".format(type(useMetro)))
    
    if time and offset:
        raise ValueError('Cannot specify both time and offset.')

    if time:
        if isinstance(time, datetime):
            params['date'] = time.strftime(DATE_FORMAT)
            params['time'] = time.strftime(TIME_FORMAT)
        else:
            raise TypeError('Expected datetime.datime, got {}.'.format(type(time)))

    if offset:
        if isinstance(offset, int):
            params['offset'] = offset
        else:
            raise TypeError("Expected <class 'int'>, got {}.".format(type(offset)))

    response = _request('departureBoard', params, timeout)
    
    result = response['DepartureBoard']

    # This key is present on error
    if 'error' in result:
        raise rjplAPIError(result['error'])

    return result['Departure']


def multiDepartureBoard(*ids, **args):
    """ Retrieve multiple station departure boards at once.

     Args:
        *args: Variable length argument list: The stop ids.
        **kwargs: Keyword arguments:
            useTrain (bool): Whether to travel by train (default: True)
            useBus (bool): Whether to travel by bus (default: True)
            useMetro (bool): Whether to travel by metro (default: True)
            time (datetime): Departure date and time of the trip. (default: current server time)
            timeout (int): Timeout time of requests.get() call in seconds.

    Returns:
        A list of dictionaries, each containing departure name, time, direction and type.
        The results from all stops are mixed, but can be filtered by stop.
    """

    if len(ids) < 1:
        raise ValueError("Need at least one id.")

    params = {'id{}'.format(i+1): ids[i] for i in range(len(ids))}
    timeout = 10

    for key in args.keys():
        if key == 'time':
            if isinstance(args['time'], datetime):
                params['date'] = args['time'].strftime(DATE_FORMAT)
                params['time'] = args['time'].strftime(TIME_FORMAT)
            else:
                raise TypeError('Expected datetime.datime, got {}.'.format(type(args['time'])))

        elif key == 'useTrain':
            if isinstance(args['useTrain'], bool):
                params['useTog'] = int(args['useTrain'])
            else:
                raise TypeError("Expected <class 'bool'>, got {}.".format(type(args['useTrain'])))
       
        elif key == 'useBus':
            if isinstance(args['useBus'], bool):
                params['useBus'] = int(args['useBus'])
            else:
                raise TypeError("Expected <class 'bool'>, got {}.".format(type(args['useBus'])))

        elif key == 'useMetro':
            if isinstance(args['useMetro'], bool):
                params['useMetro'] = int(args['useMetro'])
            else:
                raise TypeError("Expected <class 'bool'>, got {}.".format(type(args['useMetro'])))

        elif key == 'timeout':
            if isinstance(args['timeout'], int):
                timeout=args['timeout']
            else:
                raise TypeError("Expected <class 'int'>, got {}.".format(type(args['timeout'])))
        
        else:
            raise ValueError("Unknown argument '{}'.".format(key))
    
    response = _request('multiDepartureBoard', params, timeout=timeout)

    result = response['MultiDepartureBoard']

    if 'error' in result:
        raise rjplAPIError(result['error'])

    return result['Departure']

def stopsNearby(coordX, coordY, maxRadius=None, maxNumber=None, timeout=5):
    """ Finds stops close to given coordinates.

    Args:
        coordX (float): Longitude.
        coordY (float): Latitude.
        maxRadius (int): The radius in meters to search within.
        maxNumber (int): The number of results to return.
        timeout (int): Timeout time of requests.get() call in seconds.

    Returns:
        A list of nearby stops where each stop is a dictionary.
    """
    params = {}
    if isinstance(coordX, float):
        params['coordX'] = int(COORDINATE_MULTIPLIER*coordX)
    else:
        raise TypeError("Expected <class 'float'>, got {}.".format(type(coordX)))

    if isinstance(coordY, float):
        params['coordY'] = int(COORDINATE_MULTIPLIER*coordY)
    else:
        raise TypeError("Expected <class 'float'>, got {}.".format(type(coordY)))

    if maxRadius is not None:
        if isinstance(maxRadius, int):
            params['maxRadius'] = maxRadius
        else:
            raise TypeError("Expected <class 'int'>, got {}.".format(type(coordX)))

    if maxNumber is not None:
        if isinstance(maxNumber, int):
            params['maxNumber'] = maxNumber
        else:
            raise TypeError("Expected <class 'int'>, got {}.".format(type(coordX)))

    response = _request('stopsNearby', params, timeout)

    result = response['LocationList']
    if 'error' in result:
        raise rjplAPIError(result['error'])
    return result.get('StopLocation', [])

if __name__ == "__main__":
    pass
