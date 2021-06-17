from fastapi.testclient import TestClient
import pytest

from .conftest import client


def test_get_pfm_memes():
    resp = client.get("/pfm/memes")
    assert resp.status_code == 200
    assert resp.json()


@pytest.mark.parametrize("topic", (["travis", "steve", "tekk", "razjar"]))
def test_get_pfm_memes_topic(topic: str):
    resp = client.get(f"/pfm/memes?topic={topic}")
    assert resp.status_code == 200
    j = resp.json()
    assert isinstance(j, list)
    assert len(j) > 0


def test_get_pfm_meme_by_id():
    resp = client.get("/pfm/memes/1")
    assert resp.status_code == 200
    assert resp.json()


def test_get_pfm_meme_not_exists():
    resp = client.get("/pfm/memes/99999999")
    assert resp.status_code == 404


@pytest.mark.skip()
def test_add_pfm_meme():
    data = {
        "topic": "test",
        "title": "test title",
        "content": "my test",
        "media_type": "txt",
    }
    resp = client.post(
        "/pfm/memes",
        json=data,
    )
    assert resp.status_code == 201

    # then try to fetch the meme

    resp = client.get("/pfm/memes?topic=test")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) == 1
    meme = j[0]
    for k, v in data.items():
        assert meme[k] == v
