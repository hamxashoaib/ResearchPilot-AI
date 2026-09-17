import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class SubqueriesSchema(BaseModel):
    subqueries: list[str] = Field(
        description="A list of targeted search queries that decompose the main topic."
    )


def decompose_query(query: str, max_subqueries: int = 4) -> list[str]:
    """Break a complex query into focused sub-queries for deep research."""
    if not query.strip() or not client:
        return [query]

    prompt = (
        f"You are a research planning assistant. Decompose the following research topic "
        f"into at most {max_subqueries} specific, non-overlapping search engine queries:\n\n"
        f"Topic: {query}"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SubqueriesSchema,
                "temperature": 0.1,
            },
        )
        data = json.loads(response.text)
        subqueries = data.get("subqueries", [])
        return subqueries[:max_subqueries] if subqueries else [query]
    except Exception as e:
        print(f"[Query Decomposer] Fallback to primary query due to error: {e}")
        return [query]