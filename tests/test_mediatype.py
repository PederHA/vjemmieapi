import pytest

from .conftest import client


def test_get_mediatypes():
    resp = client.get("/mediatypes")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_mediatypes_by_id():
    resp = client.get("/mediatypes/txt")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["media_type"] == "txt"
    assert j["description"] == "Plain text"


def test_add_mediatype():
    resp = client.post(
        "/mediatypes",
        json={
            "media_type": "test_type",
            "description": "A media type used for testing.",
        },
    )
    assert resp.status_code == 201


def test_delete_mediatype():
    resp = client.delete("/mediatypes/test_type")
    assert resp.status_code == 204
