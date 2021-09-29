import pytest


def test_select_all(client):
    res = client.get('/plans')
    assert res.status_code == 200
    data = res.get_json()
    assert 2 == len(data['plans'])


def test_select_one(client):
    res = client.get('/plans/1')
    assert res.status_code == 200
    data = res.get_json()
    assert 'Low' == data['name']


def test_not_found(client):
    res = client.get('/plans/3')
    assert res.status_code == 404
