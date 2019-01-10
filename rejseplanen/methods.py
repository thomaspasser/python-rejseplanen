"""
Python implementation of communication with Rejseplanen API.

More information about the API can be found at
https://help.rejseplanen.dk/hc/en-us/articles/214174465-Rejseplanen-s-API

"""

from datetime import datetime
import requests

_RESOURCE = 'http://xmlopen.rejseplanen.dk/bin/rest.exe/'

def departureBoard(stop_id, useTrain=None, useBus=None, useMetro=None, dateTime=None, offset=None, timeout=10):
    params = {}

    if type(stop_id) is int:
        params['id'] = stop_id
    else:
        raise TypeError("Expected <class 'int'>, got {}.".format(type(stop_id)))


    params['format'] = 'json'

    # API defaults to use all modes of transportation
    if useTrain is not None:
        if isinstance(useTrain, bool):
            params['useTog'] = int(useTrain)
        else:
            raise TypeError("Expected <class 'bool'>, got {}".format(type(useTrain)))
    if useBus is not None:
        if isinstance(useBus, bool):
            params['useBus'] = int(useBus)
        else:
            raise TypeError("Expected <class 'bool'>, got {}".format(type(useBus)))
    if useMetro is not None:
        if isinstance(useMetro, bool):
            params['useMetro'] = int(useMetro)
        else:
            raise TypeError("Expected <class 'bool'>, got {}".format(type(useMetro)))
    
    if dateTime and offset:
        raise ValueError('Cannot specify both time and offset')

    if dateTime:
        if isinstance(dateTime, datetime):
            params['date'] = dateTime.strftime("%d.%m.%y")
            params['time'] = dateTime.strftime("%H:%M")
        else:
            raise TypeError('Expected datetime.datime, got {}'.format(type(dateTime)))

    if offset:
        if isinstance(offset, int):
            params['offset'] = offset
        else:
            raise TypeError("Expected <class 'int'>, got {}".format(type(offset)))

    response = requests.get(_RESOURCE+'departureBoard', params, timeout=timeout)

    if response.status_code != 200:
        return response

    result = response.json()['DepartureBoard']

    # This key is present on error
    if 'error' in result:
        return result

    return result['Departure']

if __name__ == "__main__":
    pass