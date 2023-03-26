import pytest
import responses

from rjpl import departureBoard, rjplConnectionError


@responses.activate
def test_departureboard_no_connection():
    with pytest.raises(rjplConnectionError):
        departureBoard(8600631)


@responses.activate
def test_departureboard_base():
    responses._add_from_file(file_path="tests/responses.yaml")

    res = departureBoard(8600631)

    assert isinstance(res, list)
    assert len(res) == 20

    item = res[0]
    assert isinstance(item, dict)
    expected_keys = ['name', 'type', 'stop', 'time', 'date', 'id',
                     'line', 'messages', 'finalStop', 'direction', 'JourneyDetailRef']
    for key in expected_keys:
        assert key in item

# def departureBoard(stop_id, useTrain=True, useBus=True, useMetro=True, time=None, offset=None, timeout=10):


@responses.activate
def test_departureboard_no_train():
    responses._add_from_file(file_path="tests/responses.yaml")

    train_types = ['IC', 'LYN', 'REG', 'S', 'TOG']
    res = departureBoard(8600631, useTrain=False)

    for item in res:
        assert item['type'] not in train_types
