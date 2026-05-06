# AI Candidate Screening Tool

A Streamlit web app that automates CV-to-job-description matching using the OpenAI API. Upload a PDF CV, paste a job description, and get a structured match score with explanation.

🔗 **Live demo:** *coming soon — deploying to Streamlit Cloud*

## What it does

- 📄 Parses PDF CVs (`pypdf`)
- 🤖 Sends structured prompts to OpenAI's API
- 📊 Returns a match score (0–100%), matching skills, missing skills, and a hiring recommendation
- 🌐 Clean web UI built with Streamlit — no command line needed

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web UI
- **OpenAI API** (GPT-4 / GPT-4o)
- **pypdf** — PDF text extraction
- **python-dotenv** — secret management

## How it works

```
PDF upload  →  Text extraction  →  Prompt construction  →  OpenAI API  →  JSON parsed  →  Streamlit UI
```

## Setup (local)

```bash
git clone https://github.com/felixwslie/ai-cv-screening.git
cd ai-cv-screening

pip install -r requirements.txt

cp .env.example .env
# Open .env and paste your OpenAI API key

streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Why I built it

Built during my own job search — I wanted objective feedback on how well my CV matched a role before applying. Turned into a working tool that demonstrates a full AI automation pattern: file input → structured prompting → parsed JSON output → user-friendly UI.

## About me

Built by Felix Wise Lie — Informatik student at TU Darmstadt focused on AI-driven workflow automation.

📧 felixwslie@gmail.com · 🔗 [LinkedIn](https://linkedin.com/in/felix-wise-lie)