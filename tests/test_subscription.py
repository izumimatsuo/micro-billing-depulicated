import pytest


def test_select_all(client):
    res = client.get('/subscriptions')
    assert res.status_code == 200
    data = res.get_json()
    assert 5 == len(data['subscriptions'])


def test_select_one(client):
    res = client.get('/subscriptions/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['start_date'].startswith('2021-01-01')


def test_not_found(client):
    res = client.get('/subscriptions/6')
    assert res.status_code == 404
