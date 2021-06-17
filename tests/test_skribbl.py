import pytest

from .conftest import client


def test_get_skribbl():
    resp = client.get("/skribbl")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_skribbl_word():
    resp = client.get("/skribbl/ion hazzikostas")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["word"] == "ion hazzikostas"


def test_get_skribbl_word_not_exists():
    resp = client.get("/skribbl/some_word_that_does_not_exist")
    assert resp.status_code == 404


def test_add_skribbl_word():
    resp = client.post(
        "/skribbl",
        json={"word": "test word", "submitter": "tester"},
    )
    assert resp.status_code == 201
    j = resp.json()
    assert j["word"] == "test word"
    assert j["submitter"] == "tester"


def test_add_existing_skribbl_word():
    resp = client.post(
        "/skribbl",
        json={"word": "test word", "submitter": "tester"},
    )
    assert resp.status_code == 400


def test_delete_skribbl_word():
    resp = client.delete("/skribbl/test word")
    assert resp.status_code == 204
    resp = client.get("/skribbl/test word")
    assert resp.status_code == 404
