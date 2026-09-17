import os
import html
import textwrap
import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/research"
)

st.set_page_config(
    page_title="ResearchPilot AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Global Styling
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    #MainMenu, footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(0, 210, 255, 0.06), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(0, 230, 118, 0.035), transparent 25%),
            #0A0F1A;
        color: #E8EEF7;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0D1422;
        border-right: 1px solid #1C293D;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-section {
        color: #738197;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    .sidebar-status {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 10px;
        background: #111B2B;
        border: 1px solid #1E2D44;
        border-radius: 8px;
        font-size: 0.74rem;
        color: #CBD5E1;
        margin-bottom: 6px;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #00E676;
        box-shadow: 0 0 9px rgba(0, 230, 118, 0.6);
    }

    .sidebar-note {
        color: #68778E;
        font-size: 0.7rem;
        line-height: 1.5;
        margin-top: 12px;
    }

    /* Hero */
    .hero {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
        margin-bottom: 16px;
    }

    .hero-left {
        max-width: 850px;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #00D2FF;
        background: rgba(0, 210, 255, 0.08);
        border: 1px solid rgba(0, 210, 255, 0.22);
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .hero-title {
        margin: 0;
        color: #FFFFFF;
        font-size: 2.1rem;
        line-height: 1.05;
        letter-spacing: -0.04em;
        font-weight: 800;
    }

    .hero-description {
        color: #8593A9;
        font-size: 0.82rem;
        margin-top: 6px;
        line-height: 1.5;
    }

    .hero-status {
        min-width: 170px;
        padding: 10px 12px;
        background: #101928;
        border: 1px solid #1D2C42;
        border-radius: 10px;
    }

    .hero-status-label {
        color: #66758B;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
    }

    .hero-status-value {
        color: #00E676;
        font-size: 0.80rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Card Box */
    .card {
        background: rgba(15, 24, 39, 0.92);
        border: 1px solid #1B2A40;
        border-radius: 11px;
        padding: 14px 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
    }

    .input-label {
        color: #A8B4C5;
        font-size: 0.70rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    div[data-testid="stTextInput"] input {
        background: #0E1726 !important;
        color: #F8FAFC !important;
        border: 1px solid #26364D !important;
        border-radius: 8px !important;
        min-height: 40px !important;
        font-size: 0.80rem !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #00BFFF !important;
        box-shadow: 0 0 0 1px rgba(0, 191, 255, 0.2) !important;
    }

    .stButton > button {
        border-radius: 7px !important;
        min-height: 38px !important;
        font-weight: 700 !important;
        font-size: 0.74rem !important;
        transition: 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00A3FF, #00D2FF) !important;
        border: none !important;
        color: #06101D !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #00BFFF !important;
    }

    /* Compact Metrics Boxes Before Summary */
    .metric-card {
        background: #0F1828;
        border: 1px solid #1B2A40;
        border-radius: 10px;
        padding: 10px 14px;
        min-height: 72px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .metric-label {
        color: #728097;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        line-height: 1;
    }

    .metric-value {
        color: #F8FAFC;
        font-family: "JetBrains Mono", monospace;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 4px;
        line-height: 1.1;
    }

    .metric-caption {
        color: #5F7088;
        font-size: 0.64rem;
        margin-top: 2px;
        line-height: 1;
    }

    /* Compact Welcome Banner */
    .welcome-panel {
        min-height: 80px;
        display: flex;
        flex-direction: row;
        align-items: center;
        text-align: left;
        padding: 14px 18px;
        gap: 14px;
        background: linear-gradient(145deg, rgba(17, 28, 46, 0.96), rgba(11, 18, 31, 0.96));
        border: 1px solid #1D2D44;
        border-radius: 11px;
        position: relative;
        overflow: hidden;
    }

    .welcome-panel::before {
        content: "";
        position: absolute;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: rgba(0, 210, 255, 0.04);
        filter: blur(25px);
        top: -70px;
        left: 20px;
    }

    .welcome-icon {
        width: 36px;
        height: 36px;
        min-width: 36px;
        border-radius: 9px;
        background: #101F32;
        border: 1px solid #21405A;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00D2FF;
        font-size: 18px;
        margin-bottom: 0;
        position: relative;
    }

    .welcome-title {
        color: #FFFFFF;
        font-size: 0.90rem;
        font-weight: 700;
        position: relative;
    }

    .welcome-text {
        color: #718097;
        font-size: 0.70rem;
        line-height: 1.4;
        margin-top: 2px;
        position: relative;
    }

    /* Compact Feature Cards */
    .feature-card {
        background: #0F1828;
        border: 1px solid #1B2A40;
        border-radius: 10px;
        padding: 10px 12px;
        min-height: 82px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .feature-head {
        display: flex;
        align-items: center;
        gap: 7px;
        margin-bottom: 4px;
    }

    .feature-icon {
        color: #00D2FF;
        font-size: 15px;
        line-height: 1;
    }

    .feature-title {
        color: #EAF0F7;
        font-size: 0.74rem;
        font-weight: 700;
        line-height: 1;
    }

    .feature-text {
        color: #697990;
        font-size: 0.65rem;
        line-height: 1.4;
    }

    /* Reports & Sources */
    .report-card {
        background: #0F1828;
        border: 1px solid #1B2A40;
        border-radius: 11px;
        padding: 20px;
    }

    .section-heading {
        color: #FFFFFF;
        font-size: 0.88rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .source-row {
        padding: 11px 0;
        border-bottom: 1px solid #1A273A;
    }

    .source-id {
        color: #00D2FF;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.66rem;
        font-weight: 700;
    }

    .source-title {
        color: #DCE5F0;
        font-size: 0.74rem;
        font-weight: 600;
        margin-top: 2px;
    }

    .source-url {
        color: #60718A;
        font-size: 0.62rem;
        margin-top: 2px;
        word-break: break-all;
    }

    div[data-testid="stStatus"] {
        background: #0E1726 !important;
        border: 1px solid #203149 !important;
        border-radius: 9px !important;
    }

    /* Footer */
    .footer {
        border-top: 1px solid #18263A;
        margin-top: 24px;
        padding-top: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .footer-text {
        color: #596A82;
        font-size: 0.67rem;
    }

    .footer-name {
        color: #C9D4E2;
        font-weight: 700;
    }

    .footer-links {
        display: flex;
        gap: 8px;
    }

    .footer-links a {
        color: #718198;
        text-decoration: none;
        font-size: 0.67rem;
        padding: 5px 8px;
        border: 1px solid #1B2A3E;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .footer-links a:hover {
        color: #00D2FF;
        border-color: #23435C;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "active_research" not in st.session_state:
    st.session_state.active_research = None

if "research_query" not in st.session_state:
    st.session_state.research_query = ""


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-section">System</div>', unsafe_allow_html=True)
    st.markdown(
        textwrap.dedent("""\
        <div class="sidebar-status">
            <span class="status-dot"></span> Application Ready
        </div>
        <div class="sidebar-status">
            <span class="status-dot"></span> Research Engine Connected
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Pipeline Controls</div>', unsafe_allow_html=True)
    deep_mode = st.toggle(
        "Query Decomposition",
        value=False,
        help="Break complex research questions into multiple research stages.",
    )

    max_sources = st.slider(
        "Source Limit",
        min_value=3,
        max_value=8,
        value=3,
    )

    verify_claims = st.toggle(
        "Evidence Verification",
        value=True,
        help="Verify extracted claims against retrieved source material.",
    )

    st.markdown('<div class="sidebar-section">Supported Workflow</div>', unsafe_allow_html=True)
    st.markdown(
        textwrap.dedent("""\
        <div class="sidebar-note">
            Research objective → web retrieval → source scoring →
            grounded synthesis → citation validation → evidence verification.
        </div>
        """),
        unsafe_allow_html=True,
    )


# ============================================================
# Main Header
# ============================================================

st.markdown(
    textwrap.dedent("""\
    <div class="hero">
        <div class="hero-left">
            <div class="eyebrow">● Evidence-Grounded Intelligence</div>
            <h1 class="hero-title">ResearchPilot AI</h1>
            <div class="hero-description">
                A research intelligence pipeline that retrieves web evidence,
                ranks sources, generates grounded reports, and validates
                citations against retrieved evidence.
            </div>
        </div>
        <div class="hero-status">
            <div class="hero-status-label">Platform Status</div>
            <div class="hero-status-value">● Operational</div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# Research Input
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Research Objective</div>', unsafe_allow_html=True)

query_input = st.text_input(
    "Research Objective",
    placeholder="Example: What are the major developments and challenges in autonomous AI agents?",
    label_visibility="collapsed",
    key="research_query",
)

col_run, col_sample1, col_sample2 = st.columns([1.35, 1, 1], gap="small")

with col_run:
    run_btn = st.button("Execute Research Pipeline", type="primary", use_container_width=True)

with col_sample1:
    sample_1 = st.button("Try: AI Agents", use_container_width=True)

with col_sample2:
    sample_2 = st.button("Try: Quantum Computing", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# Sample Queries
# ============================================================

if sample_1:
    st.session_state.research_query = "Recent developments and practical challenges in autonomous AI agents"
    st.rerun()

if sample_2:
    st.session_state.research_query = "Recent breakthroughs and challenges in fault-tolerant quantum computing"
    st.rerun()


# ============================================================
# Execute Research Pipeline
# ============================================================

if run_btn:
    query = query_input.strip()

    if not query:
        st.warning("Enter a research objective before starting the pipeline.")
    else:
        with st.status("Running ResearchPilot pipeline...", expanded=True) as status:
            st.write("Retrieving relevant web evidence...")
            st.write("Ranking sources by quality and relevance...")
            st.write("Generating grounded research synthesis...")

            if verify_claims:
                st.write("Validating claims against retrieved evidence...")

            try:
                payload = {
                    "query": query,
                    "max_results": max_sources,
                    "deep_research": deep_mode,
                    "verify_evidence": verify_claims,
                }

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=180,
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.active_research = data
                    status.update(
                        label="Research pipeline completed",
                        state="complete",
                        expanded=False,
                    )
                    st.rerun()

                elif response.status_code == 429:
                    status.update(
                        label="API quota temporarily unavailable",
                        state="error",
                        expanded=False,
                    )
                    st.error(
                        "The Gemini API quota has been reached. "
                        "The backend is responding correctly, but the "
                        "LLM provider cannot currently accept another request."
                    )

                else:
                    status.update(
                        label=f"Backend returned HTTP {response.status_code}",
                        state="error",
                        expanded=False,
                    )
                    try:
                        error_data = response.json()
                        detail = error_data.get("detail", "Unknown backend error.")
                    except ValueError:
                        detail = response.text

                    st.error(str(detail))

            except requests.exceptions.Timeout:
                status.update(label="Research request timed out", state="error", expanded=False)
                st.error("The research pipeline took longer than expected. Please check the backend terminal.")

            except requests.exceptions.ConnectionError:
                status.update(label="Backend unavailable", state="error", expanded=False)
                st.error("Could not connect to the FastAPI backend. Make sure main.py is running on port 8000.")

            except requests.exceptions.RequestException as exc:
                status.update(label="Request failed", state="error", expanded=False)
                st.error(f"Request error: {exc}")


# ============================================================
# Current Research View
# ============================================================

research = st.session_state.get("active_research")


# ============================================================
# Initial Dashboard (Compact Boxes with Retained Icons)
# ============================================================

if not research:
    st.markdown(
        textwrap.dedent("""\
        <div class="welcome-panel">
            <div class="welcome-icon">⚡</div>
            <div>
                <div class="welcome-title">Ready for your next research question</div>
                <div class="welcome-text">
                    Enter a research objective above to retrieve web evidence,
                    evaluate source quality, generate an evidence-grounded report,
                    and validate its citations.
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.write("")

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("⌕", "Web Evidence", "Retrieve relevant information from external web sources."),
        ("◈", "Source Scoring", "Evaluate retrieved sources using quality and relevance signals."),
        ("✦", "Grounded Synthesis", "Generate a structured report using retrieved evidence as context."),
        ("✓", "Evidence Verification", "Validate citations and audit claims against source material."),
    ]

    for column, feature in zip([f1, f2, f3, f4], features):
        with column:
            icon, title, description = feature
            clean_feature_html = (
                f'<div class="feature-card">'
                f'<div class="feature-head">'
                f'<span class="feature-icon">{icon}</span>'
                f'<span class="feature-title">{html.escape(title)}</span>'
                f'</div>'
                f'<div class="feature-text">{html.escape(description)}</div>'
                f'</div>'
            )
            st.markdown(clean_feature_html, unsafe_allow_html=True)


# ============================================================
# Research Results View (Compact Metric Boxes Before Summary)
# ============================================================

else:
    sources = research.get("sources", [])
    validation = research.get("citation_validation", {})
    report = research.get("report", "")

    valid_citations = validation.get("valid_citations", [])
    invalid_citations = validation.get("invalid_citations", [])

    total_sources = len(sources)
    valid_count = len(valid_citations)
    invalid_count = len(invalid_citations)

    citation_state = "Validated" if validation.get("is_valid", False) else "Review required"

    # --------------------------------------------------------
    # Compact Metrics Ribbon (Height Reduced)
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Sources Retrieved</div>'
            f'<div class="metric-value">{total_sources}</div>'
            f'<div class="metric-caption">Retrieved evidence set</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Valid Citations</div>'
            f'<div class="metric-value">{valid_count}</div>'
            f'<div class="metric-caption">References detected</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Invalid Citations</div>'
            f'<div class="metric-value">{invalid_count}</div>'
            f'<div class="metric-caption">IDs outside source set</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with m4:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">Citation State</div>'
            f'<div class="metric-value" style="font-size: 1.0rem;">{html.escape(citation_state)}</div>'
            f'<div class="metric-caption">Validation result</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    view = st.segmented_control(
        "Research Views",
        options=["Research Report", "Evidence Sources"],
        default="Research Report",
        label_visibility="collapsed",
    )

    st.write("")

    # --------------------------------------------------------
    # Report View
    # --------------------------------------------------------

    if view == "Research Report":
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Research Synthesis</div>', unsafe_allow_html=True)

        if report:
            st.markdown(report)
        else:
            st.info("No research report was returned by the backend.")

        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")

        if report:
            st.download_button(
                label="Download Research Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

    # --------------------------------------------------------
    # Evidence Sources View
    # --------------------------------------------------------

    else:
        st.markdown(
            textwrap.dedent("""\
            <div class="card">
                <div class="section-heading">Retrieved Evidence</div>
                <div class="card-description">Sources returned by the research pipeline.</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        st.write("")

        if not sources:
            st.info("No sources were returned.")
        else:
            for source in sources:
                source_id = source.get("id", "")
                title = source.get("title", "Untitled source")
                url = source.get("url", "")
                quality = source.get("quality_score", None)
                relevance = source.get("relevance_score", None)
                final_score = source.get("final_score", None)

                score_parts = []
                if quality is not None:
                    score_parts.append(f"Quality {float(quality):.2f}")
                if relevance is not None:
                    score_parts.append(f"Relevance {float(relevance):.2f}")
                if final_score is not None:
                    score_parts.append(f"Final {float(final_score):.2f}")

                score_text = " · ".join(score_parts)
                score_html = f'<div class="source-url">{html.escape(score_text)}</div>' if score_text else ""

                row_html = (
                    f'<div class="source-row">'
                    f'<div class="source-id">SOURCE {html.escape(str(source_id))}</div>'
                    f'<div class="source-title">{html.escape(str(title))}</div>'
                    f'<div class="source-url">{html.escape(str(url))}</div>'
                    f'{score_html}'
                    f'</div>'
                )
                st.markdown(row_html, unsafe_allow_html=True)


# ============================================================
# Footer with SVG Icons
# ============================================================

footer_html = (
    '<div class="footer">'
    '<div class="footer-text">'
    'Built by <span class="footer-name">Hamza Shoaib</span> · AI & Machine Learning Engineer'
    '</div>'
    '<div class="footer-links">'
    '<a href="https://hamzashoaib.dev" target="_blank">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="#00E676">'
    '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>'
    '</svg>'
    '<span>Portfolio</span>'
    '</a>'
    '<a href="https://github.com/hamxashoaib" target="_blank">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="#FFFFFF">'
    '<path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>'
    '</svg>'
    '<span>GitHub</span>'
    '</a>'
    '<a href="https://linkedin.com/in/ch-hamza-shoaib" target="_blank">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="#00D2FF">'
    '<path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>'
    '</svg>'
    '<span>LinkedIn</span>'
    '</a>'
    '</div>'
    '</div>'
)

st.markdown(footer_html, unsafe_allow_html=True)