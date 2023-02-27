import pytest
from world_spc.resources import grid


query = []
query.append('/grid')
query.append('?region=mida')
query.append('&start=2023-02-27T12:00:00')
query.append('&end=2023-02-27T13:00:00')

bad_query = []
bad_query.append('/grid')
bad_query.append('?regin=mida')
bad_query.append('&start=202-03-3T11:03:01')
bad_query.append('&end=2038-03-33T12:00:00')


def test_basic_get(client):
    assert client.get(''.join(query)).status_code == 200


def test_data_validation(client):
    response = client.get(''.join(bad_query))
    assert response.status_code == 400
    assert b'Not a valid datetime' in response.data


def test_for_fuel_types(client):
    response = client.get(''.join(query))
    fuel_types = [b'Wind',
                  b'Solar',
                  b'Hydro',
                  b'Other',
                  b'Petroleum',
                  b'Natural gas',
                  b'Coal',
                  b'Nuclear']
    for type in fuel_types:
        assert type in response.data
