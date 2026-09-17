# ResearchPilot AI

**ResearchPilot AI** is an evidence-grounded research platform that turns a research question into a structured, source-backed report.

Instead of asking an AI model to answer a question only from its existing knowledge, ResearchPilot first searches the web for relevant information, evaluates the retrieved sources, generates a report from that evidence, and then checks the citations and important claims.

The goal is simple: **make AI-assisted research more grounded, transparent, and reliable.**

## Why ResearchPilot?

AI models can sometimes produce incorrect information or provide citations that do not properly support their claims.

ResearchPilot uses a multi-stage research pipeline to reduce this problem.

It works more like a research assistant:

1. Understand the research objective
2. Break complex questions into focused queries
3. Search the web for relevant sources
4. Clean and remove duplicate results
5. Evaluate source quality and relevance
6. Rank the strongest sources
7. Generate a research report using the retrieved evidence
8. Validate the citations used in the report
9. Verify important claims against the original source content

This creates a research workflow where the generated report can be traced back to the evidence used to produce it.

## How It Works

```text
Research Question
        |
        v
Query Decomposition
        |
        v
Tavily Web Search
        |
        v
Source Cleaning and Aggregation
        |
        v
Quality and Relevance Scoring
        |
        v
Source Ranking
        |
        v
Gemini Research Synthesis
        |
        v
Citation Validation
        |
        v
Evidence Verification
        |
        v
Research Dashboard
```

## Key Features

### Query Decomposition

Complex research questions can be divided into smaller, focused search queries.

This allows ResearchPilot to explore different parts of a topic instead of relying on a single broad search.

### Live Web Retrieval

ResearchPilot uses the Tavily API to retrieve current information from the web.

The retrieved sources become the evidence used during the research process.

### Source Quality and Relevance Scoring

Retrieved sources are evaluated before they are used for synthesis.

The system considers factors such as:

* Source quality
* Domain credibility
* Relevance to the research question
* Overall source score

This helps prioritize stronger and more relevant sources.

### Source Aggregation

Results from multiple searches can contain duplicate pages or repeated information.

ResearchPilot cleans and combines the retrieved results so the final evidence set is more organized and useful.

### Grounded Research Synthesis

Google Gemini generates the final research report using the retrieved sources as its research context.

The goal is to keep the generated report connected to the evidence collected during the pipeline.

### Citation Validation

ResearchPilot checks citation references used in the generated report.

For example, if the report contains `[1]`, `[2]`, or `[3]`, the system checks whether those citation IDs actually exist in the retrieved source list.

### Evidence Verification

Important claims from the generated report are checked against the retrieved source content.

Claims are classified based on the available evidence as:

* **SUPPORTED**
* **UNCERTAIN**
* **UNSUPPORTED**

This provides an additional verification layer after report generation.

### Research Dashboard

The Streamlit dashboard provides a simple interface for:

* Entering research questions
* Running the research pipeline
* Viewing research reports
* Reviewing retrieved sources
* Checking citation validation
* Reviewing evidence verification results
* Downloading the generated report

## Technology Stack

| Component        | Technology                |
| ---------------- | ------------------------- |
| Frontend         | Streamlit                 |
| Backend          | FastAPI                   |
| API Server       | Uvicorn                   |
| Web Search       | Tavily API                |
| Language Model   | Google Gemini             |
| Data Validation  | Pydantic                  |
| Backend Hosting  | Render                    |
| Frontend Hosting | Streamlit Community Cloud |

## Project Structure

```text
ResearchPilot/
|
├── app/
|   ├── main.py
|   └── services/
|       ├── citation_validator.py
|       ├── deep_research.py
|       ├── evidence_verifier.py
|       ├── llm_service.py
|       ├── query_decomposer.py
|       ├── relevance.py
|       ├── search_service.py
|       ├── source_aggregator.py
|       └── source_quality.py
|
├── streamlit_app.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## What Each Service Does

### `app/main.py`

The FastAPI entry point.

It receives research requests, coordinates the different research stages, and returns the final research response.

### `citation_validator.py`

Checks whether citation references in the generated report correspond to actual retrieved sources.

### `deep_research.py`

Handles the deeper research workflow by coordinating multiple research queries and search passes.

### `evidence_verifier.py`

Checks important claims from the generated report against the retrieved source content.

### `llm_service.py`

Handles communication with Google Gemini and manages the report generation process.

### `query_decomposer.py`

Breaks complex research questions into smaller and more focused research queries.

### `relevance.py`

Measures how closely a retrieved source matches the research objective.

### `search_service.py`

Handles Tavily web searches and prepares the retrieved source data for the rest of the pipeline.

### `source_aggregator.py`

Combines results from different searches, removes duplicates, and organizes the source collection.

### `source_quality.py`

Evaluates the quality and credibility of retrieved sources.

### `streamlit_app.py`

Provides the user-facing research dashboard.

It communicates with the FastAPI backend and displays the research report, sources, metrics, and verification results.

## Getting Started

### Requirements

Before running ResearchPilot AI, make sure you have:

* Python 3.11 or newer
* A Tavily API key
* A Google AI Studio API key
* Git

## Clone the Repository

```bash
git clone https://github.com/hamxashoaib/ResearchPilot-AI.git
cd ResearchPilot
```

## Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Add your API configuration:

```env
TAVILY_API_KEY=your_tavily_key_here
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-3.5-flash
API_URL=http://127.0.0.1:8000/research
```

Replace the placeholder values with your actual API keys.

**Important:** Never commit your `.env` file or API keys to GitHub.

Make sure `.env` is included in `.gitignore`.

## Running ResearchPilot AI Locally

ResearchPilot AI has two parts:

1. FastAPI backend
2. Streamlit dashboard

Both need to be running at the same time.

### Step 1: Start the Backend

Open a terminal in the project directory and run:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

You can also open the interactive FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

The `/health` endpoint can be used to check whether the backend is running:

```text
http://127.0.0.1:8000/health
```

### Step 2: Start the Dashboard

Open a second terminal in the same project directory.

Activate the virtual environment if needed, then run:

```bash
streamlit run streamlit_app.py
```

The Streamlit dashboard will normally open at:

```text
http://localhost:8501
```

## Using the Dashboard

Once the dashboard is open:

1. Enter a research question.
2. Choose the desired research settings.
3. Start the research pipeline.
4. ResearchPilot retrieves web sources.
5. Sources are cleaned and evaluated.
6. The strongest sources are used for synthesis.
7. Gemini generates the research report.
8. Citations are validated.
9. Claims are checked against the retrieved evidence.
10. Review the final report and supporting sources in the dashboard.

## Example Research Questions

You can use questions such as:

```text
What are the major developments in autonomous AI agents?
```

```text
What are the recent breakthroughs in fault-tolerant quantum computing?
```

```text
What are the current challenges of retrieval augmented generation?
```

```text
How are AI coding agents changing software development?
```

The quality of the final research output depends on the quality and availability of the retrieved web evidence.

## API Endpoints

### Health Check

```http
GET /health
```

Returns the current backend status.

Example response:

```json
{
  "status": "healthy",
  "service": "ResearchPilot AI"
}
```

### Research

```http
POST /research
```

Starts the complete research pipeline.

Example request:

```json
{
  "query": "Recent developments in autonomous AI agents",
  "max_results": 5,
  "deep_research": false,
  "verify_evidence": true
}
```

The response contains:

* Research query
* Generated report
* Retrieved sources
* Citation validation results
* Evidence verification results
* Evidence summary

## Deployment

ResearchPilot can be deployed as two separate services.

### Backend

Deploy the FastAPI application as a Web Service on Render.

The backend requires the necessary environment variables, including:

```text
TAVILY_API_KEY
GEMINI_API_KEY
GEMINI_MODEL
```

The backend start command can be configured as:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend

Deploy `streamlit_app.py` using Streamlit Community Cloud.

Configure the `API_URL` environment variable to point to the deployed FastAPI `/research` endpoint.

For example:

```text
API_URL=https://your-backend-url/research
```

The exact deployment URL depends on the service configuration.

## Important Notes

ResearchPilot AI is designed to make AI-assisted research more grounded, but it should not be treated as a replacement for expert research or professional judgment.

Web sources can contain outdated, incomplete, or incorrect information.

The verification system provides an additional evidence check, but users should still review important sources themselves.

## Future Improvements

Potential improvements include:

* More advanced query planning
* Better source credibility evaluation
* Improved claim level verification
* More detailed evidence visualization
* Additional search providers
* Export options for different report formats
* Research history and saved reports
* More advanced research workflows

## 👨‍💻 Author

**Hamza Shoaib**

AI & ML Engineer

### Connect

* **[Portfolio](https://hamzashoaib.dev)**
* **[GitHub](https://github.com/hamxashoaib)**
* **[LinkedIn](https://www.linkedin.com/in/ch-hamza-shoaib/)**


## ⭐ Project

If you find TriageFlow interesting, consider giving the repository a ⭐ on GitHub.


