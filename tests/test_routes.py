"""End-to-end tests for the HTTP routes, exercised through the ASGI app.

These run against the real app (with its lifespan seed) backed by a temporary
SQLite database configured in conftest.py.
"""


def test_health_returns_healthy(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_home_page_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    body = resp.text
    assert "Hi, I'm Logan Kania." in body
    assert "<title>Home · Logan Kania</title>" in body


def test_resume_page_renders(client):
    resp = client.get("/resume")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Resume" in resp.text
    # The download link to the static PDF should be present.
    assert "/static/resume.pdf" in resp.text


def test_projects_page_lists_seeded_projects(client):
    resp = client.get("/projects")
    assert resp.status_code == 200
    body = resp.text
    # Both seeded projects appear...
    assert "This Website" in body
    assert "Coming soon" in body
    # ...and the tech line is rendered for the project that has one.
    assert "FastAPI · PostgreSQL · Docker · Terraform · AWS" in body


def test_projects_tech_omitted_when_absent(client):
    """The second seed project has ``tech=None``; its <p class="tech"> block
    should be skipped while the first project's tech line is still shown."""
    body = client.get("/projects").text
    # Exactly one rendered tech paragraph (only the first project has tech).
    assert body.count('<p class="tech">') == 1


def test_unknown_path_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404


def test_nav_links_present_on_every_page(client):
    for path in ("/", "/projects", "/resume"):
        body = client.get(path).text
        assert '<a href="/projects">Projects</a>' in body
        assert '<a href="/resume">Resume</a>' in body
