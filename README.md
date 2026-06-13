
# AI Resume Screener

> Upload a job description and a resume — get a ranked match score with reasoning in seconds.

Built for recruitment agencies and staffing firms drowning in manual resume screening. Turns a 15-20 minute manual review into a 2-minute AI-scored result.

---

## What it does

- Paste a job description and a candidate resume
- AI scores the candidate (0-100) against the role's required skills
- Returns a clear breakdown: what matches, what's missing
- Strict scoring rubric — no inflated "everyone's a fit" results

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| AI Orchestration | LangChain |
| LLM | Groq |
| Language | Python 3.12 |
| Deployment | Railway / Render |

---

## How It Works

1. Recruiter pastes the job description and a candidate's resume text
2. A LangChain prompt chain sends both to the LLM with a strict scoring rubric:
   - Starts at 100
   - Deducts points for each required skill that's missing or only adjacent
   - Caps inflated scores — most candidates won't break 75 unless they match nearly every requirement
3. Returns structured JSON: `score`, `reason`, `candidate name`
4. UI renders a color-coded result card (green / amber / red)

---

## Setup

```bash
git clone https://github.com/recruitment-ai-beast/recruiter-screener-ai.git
cd recruiter-screener-ai
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your-key-here
Run:

```bash
streamlit run screener-app.py
```

---
## Live Demo

🔗 [Coming soon — deployment in progress]
## Roadmap

- [ ] Bulk resume upload (screen 20+ candidates per job at once)
- [ ] PDF/DOCX file parsing (no manual copy-paste)
- [ ] Exportable ranked CSV report
- [ ] AI-generated job description tool
- [ ] AI candidate outreach message generator

---

## About

Built by a Vertical AI Engineer specializing in recruitment automation — using LangChain, RAG, and AI agents to eliminate manual workflows for staffing agencies.

**Connect:** [LinkedIn](https://www.linkedin.com/in/beast-builds-ai/) |  [GitHub](
) |  [Twitter](https://x.com/beastbuildsai)

---

*This is a working MVP, actively being developed based on real recruiter feedback.*