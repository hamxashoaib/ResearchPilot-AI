import re
from typing import Any


def calculate_relevance(query: str, source: dict[str, Any]) -> float:
    """Calculates query-source lexical overlap score between 0.0 and 1.0."""
    if not query or not query.strip():
        return 0.0

    content = (source.get("content", "") + " " + source.get("title", "")).lower()
    if not content.strip():
        return 0.0

    query_tokens = set(re.findall(r"\b[a-zA-Z0-9]{3,}\b", query.lower()))
    if not query_tokens:
        return 0.50

    matches = sum(1 for token in query_tokens if token in content)
    ratio = matches / len(query_tokens)

    # 40% base confidence + 60% proportional match
    score = 0.40 + (ratio * 0.60)
    return max(0.0, min(1.0, round(score, 2)))