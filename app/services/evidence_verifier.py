import re
from typing import Any
from app.services.llm_service import verify_claims_with_sources


def remove_sources_section(report: str) -> str:
    if not report:
        return ""
    return re.split(r"\n##\s+Sources\b", report, maxsplit=1, flags=re.IGNORECASE)[0].strip()


def extract_claims_from_report(report: str) -> list[dict[str, Any]]:
    cleaned = remove_sources_section(report)
    claims = []
    claim_id = 1

    for line in cleaned.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("SOURCE ID:"):
            continue

        citation_matches = re.findall(r"\[([0-9,\s]+)\]", line)
        if not citation_matches:
            continue

        citation_numbers = []
        for block in citation_matches:
            for num in re.findall(r"\d+", block):
                citation_numbers.append(int(num))

        if not citation_numbers:
            continue

        claim_text = re.sub(r"\s*\[[0-9,\s]+\]", "", line).strip()
        if not claim_text:
            continue

        claims.append({
            "claim_id": claim_id,
            "claim": claim_text,
            "citation": list(dict.fromkeys(citation_numbers)),
        })
        claim_id += 1

    return claims


def calculate_evidence_summary(evidence_results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(evidence_results)
    supported = sum(1 for r in evidence_results if str(r.get("status")).upper() == "SUPPORTED")
    unsupported = sum(1 for r in evidence_results if str(r.get("status")).upper() == "UNSUPPORTED")
    uncertain = sum(1 for r in evidence_results if str(r.get("status")).upper() == "UNCERTAIN")

    return {
        "total_claims": total,
        "supported_claims": supported,
        "unsupported_claims": unsupported,
        "uncertain_claims": uncertain,
        "support_rate": round(supported / total, 3) if total > 0 else 0.0,
    }


def verify_report_evidence(
    report: str,
    search_results: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    claims = extract_claims_from_report(report)
    if not claims or not search_results:
        return []

    try:
        raw_results = verify_claims_with_sources(claims, search_results)
    except Exception as exc:
        print(f"[Evidence Verification] Verification pass failed: {exc}")
        return []

    claim_lookup = {c["claim_id"]: c for c in claims}
    source_lookup = {s["id"]: s for s in search_results}

    final_results = []
    for item in raw_results:
        cid = item.get("claim_id")
        orig_claim = claim_lookup.get(cid)
        if not orig_claim:
            continue

        raw_ids = item.get("source_ids", [])
        valid_ids = [sid for sid in raw_ids if sid in source_lookup]

        final_results.append({
            "claim": orig_claim["claim"],
            "citation": orig_claim["citation"],
            "source_ids": valid_ids,
            "source_titles": [source_lookup[sid].get("title", "Untitled") for sid in valid_ids],
            "status": str(item.get("status", "UNCERTAIN")).upper(),
        })

    return final_results