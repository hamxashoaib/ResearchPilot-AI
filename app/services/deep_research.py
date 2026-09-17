from typing import Any
from app.services.query_decomposer import decompose_query
from app.services.search_service import search_web
from app.services.source_aggregator import aggregate_and_deduplicate


def deep_research_search(
    query: str,
    max_subqueries: int = 4,
    max_results_per_query: int = 4
) -> dict[str, Any]:
    """
    Executes multi-step query decomposition and aggregated web search.
    """
    if not query or not query.strip():
        raise ValueError("Research query cannot be empty.")

    query = query.strip()
    subqueries = decompose_query(query=query, max_subqueries=max_subqueries)
    if not subqueries:
        subqueries = [query]

    all_discovered = []
    for subquery in subqueries:
        try:
            results = search_web(query=subquery, max_results=max_results_per_query)
            for item in results:
                all_discovered.append({**item, "research_query": subquery})
        except Exception as e:
            print(f"[Deep Research] Search step failed for '{subquery}': {e}")
            continue

    # Deduplicate and assign sequential IDs
    final_sources = aggregate_and_deduplicate(all_discovered)

    return {
        "original_query": query,
        "subqueries": subqueries,
        "total_subqueries": len(subqueries),
        "total_sources": len(final_sources),
        "sources": final_sources,
    }