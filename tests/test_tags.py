import pytest
from fastapi.testclient import TestClient

from jotter.web import parse_tags


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("App, app ,", ["app"]),
        ("Work, work , IDEAS", ["work", "ideas"]),
        ("  side-project ,,Community", ["side-project", "community"]),
        ("b, a, B", ["b", "a"]),  # first-seen order is kept
        (" , ,", []),
        ("", []),
    ],
)
def test_parse_tags_trims_lowercases_and_dedupes(raw: str, expected: list[str]) -> None:
    assert parse_tags(raw) == expected


def test_idea_page_shows_cleaned_tags(client: TestClient) -> None:
    resp = client.post(
        "/new",
        data={"title": "Tag test", "body": "", "tags": "Work, work , IDEAS"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert resp.text.count('class="tag"') == 2
    assert '<span class="tag">work</span>' in resp.text
    assert '<span class="tag">ideas</span>' in resp.text


def test_edit_also_cleans_tags(client: TestClient) -> None:
    client.post("/new", data={"title": "Tag test", "body": "", "tags": "x"})
    resp = client.post(
        "/ideas/1/edit",
        data={"title": "Tag test", "body": "", "tags": "Home, HOME, garden"},
        follow_redirects=True,
    )
    assert resp.text.count('class="tag"') == 2
    assert '<span class="tag">home</span>' in resp.text
