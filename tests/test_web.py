from fastapi.testclient import TestClient


def create(
    client: TestClient,
    title: str = "Neighbourhood tool library",
    body: str = "Lend drills and ladders instead of everyone buying one.",
    tags: str = "community, side-project",
) -> str:
    resp = client.post(
        "/new", data={"title": title, "body": body, "tags": tags}, follow_redirects=False
    )
    assert resp.status_code == 303
    return resp.headers["location"]


def test_home_empty_state(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "No ideas yet" in resp.text


def test_create_from_form_and_view(client: TestClient) -> None:
    location = create(client)
    assert location == "/ideas/1"
    page = client.get(location).text
    assert "Neighbourhood tool library" in page
    assert "Lend drills and ladders" in page
    assert "side-project" in page


def test_idea_without_details(client: TestClient) -> None:
    location = create(client, body="")
    assert "No details yet." in client.get(location).text


def test_home_lists_ideas(client: TestClient) -> None:
    create(client, title="First")
    create(client, title="Second")
    page = client.get("/").text
    assert page.index("Second") < page.index("First")
    assert "2 ideas" in page


def test_new_form_requires_title(client: TestClient) -> None:
    resp = client.post("/new", data={"title": "  ", "body": "keep me"})
    assert resp.status_code == 400
    assert "Give your idea a short title." in resp.text
    assert "keep me" in resp.text  # draft is not lost


def test_edit_idea(client: TestClient) -> None:
    create(client)
    assert client.get("/ideas/1/edit").status_code == 200
    resp = client.post(
        "/ideas/1/edit",
        data={"title": "Tool library app", "body": "Start with a spreadsheet.", "tags": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    page = client.get("/ideas/1").text
    assert "Tool library app" in page
    assert "Start with a spreadsheet." in page


def test_delete_idea(client: TestClient) -> None:
    create(client)
    resp = client.post("/ideas/1/delete", follow_redirects=False)
    assert resp.status_code == 303
    assert client.get("/ideas/1").status_code == 404


def test_missing_idea_page_is_404(client: TestClient) -> None:
    assert client.get("/ideas/42").status_code == 404


def test_html_is_escaped(client: TestClient) -> None:
    create(client, title="<script>alert(1)</script>")
    page = client.get("/ideas/1").text
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


def test_no_public_api_or_api_docs(client: TestClient) -> None:
    for path in ("/api/ideas", "/docs", "/openapi.json"):
        assert client.get(path).status_code == 404
