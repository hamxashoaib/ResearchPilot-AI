from typing import Any


def aggregate_and_deduplicate(
    sources_list: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Combines sources from multiple searches or deep research,
    stripping duplicate URLs while preserving metadata.
    """
    seen_urls = set()
    aggregated = []

    for source in sources_list:
        url = source.get("url", "").strip()
        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        aggregated.append(source)

    # Re-index stable sequential IDs
    for idx, item in enumerate(aggregated, start=1):
        item["id"] = idx

    return aggregated