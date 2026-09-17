from urllib.parse import urlparse
from typing import Any

AUTHORITATIVE_DOMAINS = {
    "edu", "gov", "org", "ac.uk", "nature.com", "arxiv.org",
    "sciencedirect.com", "ieee.org", "reuters.com", "bloomberg.com",
    "nytimes.com", "bbc.com", "github.com"
}


def calculate_source_quality(source: dict[str, Any]) -> float:
    """Calculates a baseline source credibility score between 0.0 and 1.0."""
    score = 0.50
    url = source.get("url", "").strip()
    title = source.get("title", "").strip()
    content = source.get("content", "").strip()

    if not url:
        return 0.0

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if any(domain.endswith(ext) or ext in domain for ext in AUTHORITATIVE_DOMAINS):
        score += 0.25

    if parsed.scheme == "https":
        score += 0.05

    content_len = len(content)
    if content_len > 800:
        score += 0.15
    elif content_len > 300:
        score += 0.10
    else:
        score -= 0.20

    if len(title) >= 10 and not title.lower().startswith("untitled"):
        score += 0.05
    else:
        score -= 0.10

    return max(0.0, min(1.0, round(score, 2)))