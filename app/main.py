from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any

from app.services.search_service import search_web, process_and_rank_sources
from app.services.llm_service import execute_unified_research

app = FastAPI(title="ResearchPilot AI API", version="2.0.0")


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    max_results: int = Field(default=3, ge=1, le=8)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/research")
def run_research(req: ResearchRequest):
    try:
        # 1. Fast Tavily Search (~1 sec)
        raw_sources = search_web(query=req.query, max_results=req.max_results)
        if not raw_sources:
            raise HTTPException(status_code=404, detail="No relevant web sources found.")

        # 2. In-Memory Scoring (< 0.05 sec)
        ranked = process_and_rank_sources(req.query, raw_sources)

        # 3. Single-Pass Gemini Report + Claim Audit (~3-4 sec)
        result = execute_unified_research(req.query, ranked)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))