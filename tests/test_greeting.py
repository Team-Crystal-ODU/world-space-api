# test of simple API greeting to practice with Flask test features
import pytest
from world_spc.resources import greeting


def test_greeting(client):
    response = client.get('/')
    # note: b"str" is needed to resolve type error with response.data
    assert b"World Space" in response.data


def test_write_to_db(client):
    response = client.post('/hardware?user=ecogamer')
    # note: b"str" is needed to resolve type error with response.data
    assert b"Write succeeded." in response.data
