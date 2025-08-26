from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import re
import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def _clean_text(s: str) -> str:
    # Collapse whitespace and remove overly long runs
    s = re.sub(r"[\r\t\f]+", " ", s)
    s = re.sub(r"[\u00a0\s]+", " ", s)
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

@dataclass
class Website:
    url: str
    title: str = ""
    text: str = ""
    links: List[str] = field(default_factory=list)

    def fetch(self, timeout: float = 15.0, headers: Optional[dict] = None) -> str:
        headers = headers or DEFAULT_HEADERS
        resp = requests.get(self.url, timeout=timeout, headers=headers)
        resp.raise_for_status()
        return resp.text

    def parse(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")
        # Remove non-contenty tags
        for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "iframe"]):
            tag.decompose()

        # Title
        self.title = (soup.title.string if soup.title and soup.title.string else "").strip()

        # Extract main text
        body = soup.get_text("\n")
        body = _clean_text(body)

        # Heuristic: trim very long header/footer noise by keeping middle slice if huge
        if len(body) > 200000:
            body = body[:100000] + "\n...\n" + body[-100000:]

        self.text = body

        # Links (absolute/relative raw hrefs)
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href and not href.startswith("#"):
                links.append(href)
        self.links = list(dict.fromkeys(links))  # dedupe, keep order

    def get_contents(self) -> "Website":
        html = self.fetch()
        self.parse(html)
        return self

    def __str__(self) -> str:
        t = f"# {self.title}\n\n" if self.title else ""
        return f"{t}{self.text}"
