import os
from typing import Any
from dotenv import load_dotenv
from tavily import TavilyClient

from app.services.source_quality import calculate_source_quality
from app.services.relevance import calculate_relevance

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is not set.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results: int = 3) -> list[dict[str, Any]]:
    """Fast web search using Tavily's basic depth for sub-second retrieval."""
    if not query.strip():
        return []

    # search_depth="basic" cuts retrieval latency by over 65%
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=False,
    )
    return response.get("results", [])


def process_and_rank_sources(
    query: str,
    raw_results: list[dict[str, Any]],
    min_score_threshold: float = 0.25
) -> list[dict[str, Any]]:
    """Clean, rank, and truncate source snippets for fast LLM processing."""
    seen_urls = set()
    cleaned = []

    for item in raw_results:
        url = item.get("url", "").strip()
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        quality = calculate_source_quality(item)
        relevance = calculate_relevance(query, item)
        final_score = round((quality * 0.40) + (relevance * 0.60), 2)

        # Truncate content to 650 characters to minimize LLM prompt token latency
        raw_content = item.get("content", "").strip()
        truncated_content = raw_content[:650] + ("..." if len(raw_content) > 650 else "")

        cleaned.append({
            "title": item.get("title", "Web Source").strip(),
            "url": url,
            "content": truncated_content,
            "quality_score": quality,
            "relevance_score": relevance,
            "final_score": final_score,
        })

    cleaned.sort(key=lambda x: x["final_score"], reverse=True)
    final_sources = [s for s in cleaned if s["final_score"] >= min_score_threshold] or cleaned

    for idx, s in enumerate(final_sources, start=1):
        s["id"] = idx

    return final_sources