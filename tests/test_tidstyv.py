from typing import Dict, List
import pytest

from .conftest import client


def test_get_all_tidstyver():
    resp = client.get("/tidstyveri")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_tidstyv():
    resp = client.get("/tidstyveri/136501877452832769")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["user_id"] == "136501877452832769"
    assert j["stolen"] > 0


def test_get_tidstyv_not_exists():
    resp = client.get("/tidstyveri/non_existant_tidstyv")
    assert resp.status_code == 404


def test_add_tidstyveri():
    # this will create a record for "tester"
    inp = {
        "user_id": "tester",
        "stolen": 22.5,
    }
    resp = client.post("/tidstyveri", json=inp)
    assert resp.status_code == 201
    j = resp.json()
    assert j["user_id"] == inp["user_id"]
    assert j["stolen"] == inp["stolen"]

    # also test that we can increment the value
    resp = client.post("/tidstyveri", json=inp)
    assert resp.status_code == 201
    j = resp.json()
    assert j["user_id"] == inp["user_id"]
    assert j["stolen"] == 45.0


def test_remove_tidstyveri():
    inp = {
        "user_id": "tester",
        "stolen": 45.0,
    }
    resp = client.post("/tidstyveri?decrease=1", json=inp)
    assert resp.status_code == 201
    j = resp.json()
    assert j["user_id"] == inp["user_id"]
    assert j["stolen"] == 0.0

    # try to decrease below 0

    resp = client.post(
        "/tidstyveri?decrease=1",
        json={
            "user_id": "tester",
            "stolen": 9999999.9,
        },
    )
    j = resp.json()
    assert j["stolen"] == 0.0


def test_delete_tidstyv():
    resp = client.delete("/tidstyveri/tester")
    assert resp.status_code == 204
