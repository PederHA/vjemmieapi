from typing import Dict, List
import pytest

from .conftest import client


def _alias_exists(alias: str, aliases: List[Dict[str, str]]) -> bool:
    return any(a["alias"] == alias for a in aliases)


def test_get_all_subreddits():
    resp = client.get("/reddit/subreddits")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0


def test_get_all_text_subreddits():
    resp = client.get("/reddit/subreddits?text=1")
    assert resp.status_code == 200
    j = resp.json()
    assert len(j) > 0
    assert all(sub["subreddit"] != "totalwar" for sub in j)


def test_get_subreddit_scottishpeopletwitter():
    resp = client.get("/reddit/subreddits/scottishpeopletwitter")
    assert resp.status_code == 200
    j = resp.json()
    assert j
    assert j["subreddit"] == "scottishpeopletwitter"
    assert _alias_exists("spt", j["aliases"])


def test_add_subreddit():
    resp = client.post(
        "/reddit/subreddits",
        json={
            "subreddit": "testsubreddit",
            "is_text": False,
            "submitter": "tester",
            "aliases": ["ts"],
        },
    )
    assert resp.status_code == 201
    j = resp.json()
    assert j["subreddit"] == "testsubreddit"
    assert j["submitter"] == "tester"
    assert _alias_exists("ts", j["aliases"])


def test_add_subreddit_alias():
    resp = client.put(
        "/reddit/subreddits/testsubreddit",
        json={"aliases": [{"alias": "test", "remove": False}]},
    )
    assert resp.status_code == 200

    resp = client.get("/reddit/subreddits/testsubreddit")
    assert resp.status_code == 200
    j = resp.json()
    assert _alias_exists("test", j["aliases"])
    assert _alias_exists("ts", j["aliases"])


def test_delete_subreddit():
    resp = client.delete("/reddit/subreddits/testsubreddit")
    assert resp.status_code == 204
