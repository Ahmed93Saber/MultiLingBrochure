import types
from brochure_app.scraper import Website

SAMPLE_HTML = """
<html><head><title>Test Page</title></head>
<body>
  <nav>Menu</nav>
  <h1>Welcome</h1>
  <p>We build delightful products for data teams.</p>
  <a href="https://example.com/about">About</a>
  <footer>Footer</footer>
</body></html>
"""

class DummyResp:
    def __init__(self, text): self.text = text
    def raise_for_status(self): return None

def test_parse_without_network(monkeypatch):
    w = Website("https://example.com")

    def fake_get(url, timeout=None, headers=None):
        return DummyResp(SAMPLE_HTML)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    w.get_contents()
    assert w.title == "Test Page"
    assert "Welcome" in w.text
    assert any("about" in link for link in w.links)
