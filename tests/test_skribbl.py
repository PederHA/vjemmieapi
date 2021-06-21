import pytest

from .conftest import client


def test_get_skribbl():
    resp = client.get("/skribbl/words")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_skribbl_word():
    resp = client.get("/skribbl/words/ion hazzikostas")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["word"] == "ion hazzikostas"


def test_get_skribbl_word_not_exists():
    resp = client.get("/skribbl/words/some_word_that_does_not_exist")
    assert resp.status_code == 404


def test_add_skribbl_word():
    resp = client.post(
        "/skribbl/words",
        json={"submitter": "tester", "words": ["test word"]},
    )
    assert resp.status_code == 201
    j = resp.json()
    assert len(j["added"]) == 1
    assert j["added"][0] == "test word"


def test_add_existing_skribbl_word():
    resp = client.post(
        "/skribbl/words",
        json={"submitter": "tester", "words": ["test word"]},
    )
    j = resp.json()
    assert len(j["added"]) == 0
    assert len(j["failed"]) == 1
    assert j["failed"][0] == "test word"


def test_delete_skribbl_word():
    resp = client.delete("/skribbl/words/test word")
    assert resp.status_code == 204
    resp = client.get("/skribbl/words/test word")
    assert resp.status_code == 404
