import streamlit as st
import openai
from pypdf import PdfReader
from dotenv import load_dotenv
import os
import io
import json

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CV_CHAR_LIMIT = 8000
JD_CHAR_LIMIT = 4000


@st.cache_data
def extract_pdf(file_bytes: bytes) -> tuple[str, int]:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = "".join([p.extract_text() or "" for p in reader.pages])
    return text, len(reader.pages)


st.set_page_config(page_title="CV Analyzer | AI-Powered", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }
.main { background-color: #0f1117; }
section[data-testid="stSidebar"] { display: none; }

.hero {
    background: linear-gradient(135deg, #0a0f1e 0%, #1a237e 50%, #0d47a1 100%);
    padding: 48px 40px;
    border-radius: 16px;
    margin-bottom: 32px;
    text-align: center;
}
.hero h1 { color: white; font-size: 2.4rem; font-weight: 700; margin: 0 0 8px 0; letter-spacing: -0.5px; }
.hero p { color: #90caf9; font-size: 1.05rem; margin: 0; }

.card { background: #1e2130; border: 1px solid #2d3250; border-radius: 12px; padding: 24px; margin-bottom: 16px; }
.card-title { color: #90caf9; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.score-card {
    background: linear-gradient(135deg, #1a237e, #0d47a1);
    border-radius: 12px;
    padding: 28px;
    text-align: center;
    margin-bottom: 16px;
    border: 1px solid #1565c0;
}
.score-number { color: white; font-size: 3.5rem; font-weight: 700; line-height: 1; }
.score-label { color: #90caf9; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; }

.result-section {
    background: #1e2130;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 12px;
    border-left: 3px solid #1565c0;
}
.result-section p, .result-section li { color: #cdd6f4; font-size: 0.92rem; line-height: 1.7; margin: 0; }
.result-section ul { margin: 8px 0 0 0; padding-left: 18px; }

.stButton>button {
    background: linear-gradient(135deg, #1a237e, #0d47a1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    height: 3.2em !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}
.stButton>button:hover { opacity: 0.85 !important; }

.metric-row { display: flex; gap: 12px; margin-bottom: 16px; }
.metric-box { flex: 1; background: #1e2130; border: 1px solid #2d3250; border-radius: 10px; padding: 14px; text-align: center; }
.metric-value { color: white; font-size: 1.5rem; font-weight: 700; }
.metric-label { color: #6b7db3; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; }

.stFileUploader, .stTextArea textarea { background: #1e2130 !important; color: white !important; }

.empty-state { text-align: center; padding: 60px 20px; color: #3d4f7c; }
.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-text { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎯 CV Analyzer</h1>
    <p>AI-powered CV matching — upload a CV and get an instant fit report against any job description</p>
</div>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

col1, col2 = st.columns([1, 1.4], gap="large")

cv_text = ""
total_pages = 0
word_count = 0

with col1:
    st.markdown('<div class="card-title">📤 Input</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        cv_text, total_pages = extract_pdf(uploaded_file.read())
        word_count = len(cv_text.split())

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-value">{total_pages}</div><div class="metric-label">Pages</div></div>
            <div class="metric-box"><div class="metric-value">{word_count}</div><div class="metric-label">Words</div></div>
            <div class="metric-box"><div class="metric-value">✅</div><div class="metric-label">Ready</div></div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Preview extracted text"):
            st.caption(cv_text[:1500] + "..." if len(cv_text) > 1500 else cv_text)
    else:
        st.info("👆 Drop a PDF CV here to get started")

    st.markdown('<div class="card-title" style="margin-top:20px">💼 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

    analyze_btn = st.button("🔍 Analyze CV Now", use_container_width=True)

with col2:
    st.markdown('<div class="card-title">📊 Analysis Result</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not cv_text or not job_description:
            st.warning("⚠️ Please upload a CV and add a job description first!")
        else:
            if len(cv_text) > CV_CHAR_LIMIT:
                st.warning(f"⚠️ CV is long — only the first {CV_CHAR_LIMIT} characters will be analyzed.")
            if len(job_description) > JD_CHAR_LIMIT:
                st.warning(f"⚠️ Job description is long — only the first {JD_CHAR_LIMIT} characters will be analyzed.")

            with st.spinner("🤖 Analyzing..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        response_format={"type": "json_object"},
                        messages=[{
                            "role": "user",
                            "content": f"""
You are a senior HR recruiter. Analyze this CV against the job description.

CV:
{cv_text[:CV_CHAR_LIMIT]}

Job Description:
{job_description[:JD_CHAR_LIMIT]}

Return ONLY valid JSON with this exact structure:
{{
  "match_score": <integer 0-100>,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "verdict": "Hire" or "Maybe" or "No",
  "summary": "2-3 sentence hiring recommendation"
}}
"""
                        }]
                    )
                    st.session_state.result = json.loads(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"❌ Analysis failed: {e}")

    if st.session_state.result:
        data = st.session_state.result
        score = data.get("match_score", "–")
        verdict = data.get("verdict", "–")
        matching = data.get("matching_skills", [])
        missing = data.get("missing_skills", [])
        summary = data.get("summary", "")

        verdict_color = {"Hire": "#4caf50", "Maybe": "#ff9800", "No": "#f44336"}.get(verdict, "#90caf9")

        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{score}/100</div>
            <div class="score-label">Match Score</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-section" style="border-left-color:{verdict_color}; text-align:center;">
            <span style="color:{verdict_color}; font-size:1.2rem; font-weight:700;">RECOMMENDATION: {verdict}</span>
        </div>
        """, unsafe_allow_html=True)

        if matching:
            items = "".join(f"<li>✅ {s}</li>" for s in matching)
            st.markdown(f'<div class="result-section"><p class="card-title">Matching Skills</p><ul>{items}</ul></div>', unsafe_allow_html=True)

        if missing:
            items = "".join(f"<li>❌ {s}</li>" for s in missing)
            st.markdown(f'<div class="result-section"><p class="card-title">Missing Skills</p><ul>{items}</ul></div>', unsafe_allow_html=True)

        if summary:
            st.markdown(f'<div class="result-section"><p class="card-title">Summary</p><p>{summary}</p></div>', unsafe_allow_html=True)

        report = f"""CV MATCH REPORT
===============
Match Score : {score}/100
Verdict     : {verdict}

MATCHING SKILLS:
{chr(10).join(f"- {s}" for s in matching)}

MISSING SKILLS:
{chr(10).join(f"- {s}" for s in missing)}

SUMMARY:
{summary}
"""
        st.download_button(
            "⬇️ Download Full Report",
            data=report,
            file_name="cv_match_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    elif not analyze_btn:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎯</div>
            <div class="empty-text">Fill in the left panel and hit<br><strong>Analyze CV Now</strong></div>
        </div>
        """, unsafe_allow_html=True)
