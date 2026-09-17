import re
from typing import Any, Union


def extract_citations(report: str) -> list[int]:
    """
    Extract citation numbers from bracket patterns:
    [1], [2], [1, 2], [1, 2, 3]
    """
    if not report:
        return []

    citation_blocks = re.findall(r"\[([0-9,\s]+)\]", report)
    citations = []

    for block in citation_blocks:
        numbers = re.findall(r"\d+", block)
        for number in numbers:
            try:
                citations.append(int(number))
            except ValueError:
                continue

    return citations


def validate_citations(
    report: str,
    sources_or_count: Union[int, list[dict[str, Any]]]
) -> dict[str, Any]:
    """Validate report citations against available sources."""
    source_count = (
        len(sources_or_count)
        if isinstance(sources_or_count, list)
        else sources_or_count
    )

    if not report or source_count <= 0:
        return {
            "is_valid": False,
            "citations_found": [],
            "valid_citations": [],
            "invalid_citations": [],
        }

    citations = extract_citations(report)
    unique_citations = sorted(set(citations))

    valid_citations = [c for c in unique_citations if 1 <= c <= source_count]
    invalid_citations = [c for c in unique_citations if c < 1 or c > source_count]

    return {
        "is_valid": len(invalid_citations) == 0,
        "citations_found": unique_citations,
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations,
    }