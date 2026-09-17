import os
import json
import time
import random
from typing import Any
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

from app.services.citation_validator import validate_citations

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in the .env file.")

# Directly reads gemini-3.5-flash configured in your .env
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

MAX_RETRIES = 5
BASE_DELAY = 3.0

client = genai.Client(api_key=GEMINI_API_KEY)


class ClaimVerificationItem(BaseModel):
    claim: str = Field(description="The factual claim made in the report")
    citation: list[int] = Field(description="The source IDs cited for this claim")
    status: str = Field(description="SUPPORTED, UNCERTAIN, or UNSUPPORTED based on sources")


class UnifiedResearchOutput(BaseModel):
    report: str = Field(description="Structured markdown report with [1], [2] citations.")
    used_source_ids: list[int] = Field(description="IDs of sources cited in the report.")
    verified_claims: list[ClaimVerificationItem] = Field(
        description="Key factual claims verified directly against the provided source text."
    )


def build_compact_sources(search_results: list[dict[str, Any]]) -> str:
    return "\n---\n".join([
        f"ID: [{s.get('id')}] {s.get('title')}\nCONTENT: {s.get('content')}"
        for s in search_results
    ])


def call_gemini_35_flash(prompt: str) -> str:
    """
    Executes gemini-3.5-flash with jittered exponential backoff
    to handle 503 UNAVAILABLE traffic spikes without pipeline failure.
    """
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": 0.1,
                    "response_mime_type": "application/json",
                    "response_schema": UnifiedResearchOutput,
                },
            )
            return getattr(response, "text", "").strip()

        except Exception as exc:
            last_error = exc
            err_msg = str(exc)

            is_server_spike = (
                "503" in err_msg 
                or "UNAVAILABLE" in err_msg 
                or "high demand" in err_msg.lower()
                or "429" in err_msg
                or "RESOURCE_EXHAUSTED" in err_msg
            )

            if is_server_spike:
                if "perday" in err_msg.lower():
                    raise RuntimeError(f"Gemini Daily Quota Exceeded: {err_msg}") from exc

                # Exponential backoff with random jitter: ~3s, ~6s, ~12s...
                sleep_duration = (BASE_DELAY * (2 ** (attempt - 1))) + random.uniform(0.5, 2.0)
                print(
                    f"[{MODEL_NAME}] Server 503 spike (Attempt {attempt}/{MAX_RETRIES}). "
                    f"Retrying in {sleep_duration:.1f}s..."
                )
                time.sleep(sleep_duration)
                continue

            # Non-temporary error: break immediately
            break

    raise RuntimeError(
        f"Google Gemini ({MODEL_NAME}) is temporarily overloaded with high traffic (503 UNAVAILABLE). "
        f"Attempts exhausted: {last_error}"
    )


def execute_unified_research(query: str, search_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Single-pass synthesis and verification in a single prompt for speed."""
    if not search_results:
        raise ValueError("No search sources available.")

    sources_text = build_compact_sources(search_results)

    prompt = f"""You are a high-speed research analyst.
Analyze the provided sources and generate a concise report AND audit the claims in ONE pass.

QUERY: {query}

SOURCES:
{sources_text}

INSTRUCTIONS:
1. Write a structured markdown report (# Summary, ## Key Findings, ## Analysis, ## Sources) with [1], [2] citations.
2. Extract 4-6 key factual claims and verify each claim against the sources (SUPPORTED, UNCERTAIN, or UNSUPPORTED).
3. Do not introduce outside knowledge.
"""

    raw_json = call_gemini_35_flash(prompt)
    data = json.loads(raw_json)
    report = data.get("report", "").strip()

    # Deterministic local citation validation
    validation = validate_citations(report, len(search_results))

    # Format claims
    formatted_claims = []
    supported_count = 0
    raw_claims = data.get("verified_claims", [])

    for idx, c in enumerate(raw_claims, start=1):
        status = c.get("status", "UNCERTAIN").upper()
        if status == "SUPPORTED":
            supported_count += 1

        formatted_claims.append({
            "claim_id": idx,
            "claim": c.get("claim", ""),
            "citation": c.get("citation", []),
            "status": status,
            "source_ids": c.get("citation", []),
            "source_titles": [
                s.get("title", "") for s in search_results if s.get("id") in c.get("citation", [])
            ],
        })

    total_c = len(formatted_claims)
    support_rate = round(supported_count / total_c, 2) if total_c > 0 else 1.0

    return {
        "query": query,
        "report": report,
        "sources": search_results,
        "citation_validation": validation,
        "evidence_verification": formatted_claims,
        "evidence_summary": {
            "total_claims": total_c,
            "supported_claims": supported_count,
            "unsupported_claims": sum(1 for c in formatted_claims if c["status"] == "UNSUPPORTED"),
            "uncertain_claims": sum(1 for c in formatted_claims if c["status"] == "UNCERTAIN"),
            "support_rate": support_rate,
        },
    }