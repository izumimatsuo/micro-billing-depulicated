import pytest


def test_all_days(client):
    res = client.get('/invoices')
    assert res.status_code == 200
    assert 4 == len(res.data.splitlines())
    assert b'"name","amount","start_date"' in res.data
    assert b'"Taro",980,"2021-01-01 00:00:00"' in res.data
    assert b'"Jiro",1500,"2021-01-31 00:00:00"' in res.data
    assert b'"Hanako",980,"2021-02-28 00:00:00"' in res.data


def test_first_day(client):
    res = client.get('/invoices/20210401')
    assert res.status_code == 200
    assert 2 == len(res.data.splitlines())
    assert b'"name","amount","start_date"' in res.data
    assert b'"Taro",980,"2021-01-01 00:00:00"' in res.data


def test_last_day(client):
    res = client.get('/invoices/20210430')
    assert res.status_code == 200
    assert 2 == len(res.data.splitlines())
    assert b'"name","amount","start_date"' in res.data
    assert b'"Jiro",1500,"2021-01-31 00:00:00"' in res.data


def test_leap_year(client):
    res = client.get('/invoices/20240229')
    assert res.status_code == 200
    assert 2 == len(res.data.splitlines())
    assert b'"name","amount","start_date"' in res.data
    assert b'"Jiro",1500,"2021-01-31 00:00:00"' in res.data


def test_not_leap_year(client):
    res = client.get('/invoices/20220228')
    assert res.status_code == 200
    assert 3 == len(res.data.splitlines())
    assert b'"name","amount","start_date"' in res.data
    assert b'"Jiro",1500,"2021-01-31 00:00:00"' in res.data
    assert b'"Hanako",980,"2021-02-28 00:00:00"' in res.data


def test_bad_request(client):
    res = client.get('/invoices/20210431')
    assert res.status_code == 400
