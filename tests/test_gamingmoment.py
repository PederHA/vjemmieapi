import pytest

from .conftest import client


def test_get_gamingmoments():
    resp = client.get("/gamingmoments")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_gamingmoments_by_id():
    resp = client.get("/gamingmoments/103890994440728576")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["count"] > 0


def test_get_gamingmoments_by_id_not_exists():
    resp = client.get("/gamingmoments/some_user_id")
    assert resp.status_code == 404


def test_add_gamingmoment():
    # this will create a db entry for "tester"
    resp = client.post("/gamingmoments/tester")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 1

    # also test that we can increment the counter for "tester"
    resp = client.post("/gamingmoments/tester")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 2


def test_decrease_gamingmoment():
    # Test that we can decrease the count for "tester"
    resp = client.post("/gamingmoments/tester?decrease=1")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 1

    # Test that we can decrement to 0, but not beyond
    resp = client.post("/gamingmoments/tester?decrease=1")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 0

    # This should not go below 0
    resp = client.post("/gamingmoments/tester?decrease=1")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 0

    # Test that decreasing for an undefined user creates it and sets counter to 0
    resp = client.post("/gamingmoments/tester2?decrease=1")
    assert resp.status_code == 201
    j = resp.json()
    assert j["count"] == 0


def test_delete_gamingmoment():
    resp = client.delete("/gamingmoments/tester")
    assert resp.status_code == 204
    resp = client.delete("/gamingmoments/tester2")
    assert resp.status_code == 204
