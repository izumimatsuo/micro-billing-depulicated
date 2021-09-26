import pytest


def test_select_all(client):
    res = client.get('/customers')
    assert res.status_code == 200
    data = res.get_json()
    assert 5 == len(data['customers'])


def test_select_one(client):
    res = client.get('/customers/1')
    assert res.status_code == 200
    data = res.get_json()
    print(data)
    assert 'Taro' == data['name']


def test_not_found(client):
    res = client.get('/customers/6')
    assert res.status_code == 404

