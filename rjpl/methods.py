"""
Python implementation of communication with Rejseplanen API.

More information about the API can be found at
https://help.rejseplanen.dk/hc/en-us/articles/214174465-Rejseplanen-s-API

"""
from datetime import datetime
import requests

from .classes import Place, Stop, Coord
from .constants import *

def _request(service, params, timeout):
    params['format'] = 'json'
    

    try:
        response = requests.get(RESOURCE+service, params, timeout=timeout)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)

    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError('Error: ' + str(response.status_code) +
                str(response.content))

def location(input, timeout=5):
    params = {}

    if isinstance(input, str):
        params['input'] = input
    else:
        raise TypeError("Expected <class 'str'> got {}".format(type(input)))
    
    response = _request('location', params, timeout)

    result = response['LocationList']

    if 'error' in result:
        raise RuntimeError(result['error'])

    return result

def trip(origin, destination, viaId=None, time=None, searchForArrival=None, useTrain=True, 
         useBus=True, useMetro=True, useBicycle=False, maxWalkingDistanceDep=None, 
         maxWalkingDistanceDest=None, maxCyclingDistanceDep=None, maxCyclingDistanceDest=None, timeout=10):
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
            params['destId'] = destination.id
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
        raise RuntimeError(result['error'])

    return result['Trip']


def departureBoard(stop_id, useTrain=True, useBus=True, useMetro=True, time=None, offset=None, timeout=10):
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
        raise RuntimeError(result['error'])

    return result['Departure']


def multiDepartureBoard(*ids, **args):
    if len(ids) < 1:
        raise ValueError("Need at least one id.")

    params = {'id{}'.format(i+1): ids[i] for i in range(len(ids))}

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
        else:
            raise ValueError("Unknown argument '{}'.".format(key))
    
    response = _request('multiDepartureBoard', params, timeout=10)

    result = response['MultiDepartureBoard']

    if 'error' in result:
        raise RuntimeError(result['error'])

    return result['Departure']

def stopsNearby(coordX, coordY, maxRadius=None, maxNumber=None, timeout=5):
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

    response = _request('stopsNearby', params, timeout)

    result = response['LocationList']
    if 'error' in result:
        raise RuntimeError(result['error'])

    return result['StopLocation']


if __name__ == "__main__":
    pass
