import streamlit as st
import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="designarena_image_6fgagtj9.jpg",
    layout="wide",
)

# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #060a1a 0%, #0a1128 100%);
        color: #e6f1ff;
    }
    section[data-testid="stSidebar"] { display: none; }

    .brand-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px 24px;
        border-radius: 14px;
        background: rgba(15, 25, 55, 0.6);
        border: 1px solid rgba(77, 208, 225, 0.25);
        margin-bottom: 28px;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #ffffff;
        margin: 0;
    }
    .brand-sub {
        font-size: 13px;
        color: #7fb3c9;
        margin: 0;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        color: #4dd0e1;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }

    .stTextArea textarea {
        background-color: #0d1530 !important;
        border: 1px solid rgba(77, 208, 225, 0.2) !important;
        border-radius: 10px !important;
        color: #e6f1ff !important;
    }
    .stTextArea textarea:focus {
        border: 1px solid #4dd0e1 !important;
        box-shadow: 0 0 0 1px rgba(77,208,225,0.3) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #1ec3d6 0%, #0a6fb0 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(30, 195, 214, 0.35);
        color: #ffffff;
    }

    .result-card {
        border-radius: 14px;
        padding: 24px 28px;
        margin-top: 20px;
        background: rgba(15, 25, 55, 0.7);
        border: 1px solid rgba(77, 208, 225, 0.2);
    }
    .result-name {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .score-badge {
        display: inline-block;
        font-size: 28px;
        font-weight: 800;
        padding: 6px 18px;
        border-radius: 10px;
        margin: 10px 0 14px 0;
    }
    .score-high { background: rgba(74, 222, 128, 0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.4); }
    .score-mid  { background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.4); }
    .score-low  { background: rgba(248, 113, 113, 0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.4); }

    .reason-label {
        font-size: 12px;
        font-weight: 700;
        color: #7fb3c9;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .reason-text {
        font-size: 15px;
        line-height: 1.6;
        color: #cfe6f2;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col_logo, col_title = st.columns([1, 8])
with col_logo:
    if os.path.exists("designarena_image_6fgagtj9.jpg"):
        st.image("designarena_image_6fgagtj9.jpg", width=64)
with col_title:
    st.markdown("""
        <div style="padding-top:6px;">
            <p class="brand-title">AI Resume Screener</p>
            <p class="brand-sub">Vertical AI Engineer · Recruitment Automation</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- INPUTS ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area("", height=260, placeholder="Paste the JD here...", label_visibility="collapsed", key="jd")
with col2:
    st.markdown('<div class="section-label">Candidate Resume</div>', unsafe_allow_html=True)
    resume_text = st.text_area("", height=260, placeholder="Paste candidate resume text here...", label_visibility="collapsed", key="resume")

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("Score Resume")

if run:
    if not job_description.strip() or not resume_text.strip():
        st.warning("Paste both a job description and a resume.")

    else:
        with st.spinner("Scoring..."):
            llm = ChatGroq(model="llama-3.1-8b-instant",temperature=0)

            prompt = ChatPromptTemplate.from_template(
                """You are a strict technical recruiter. Score this resume against the job description.

Job description:
{job_description}

Resume:
{resume_text}

Scoring rules:
- Start at 100.
- For each REQUIRED skill/tool explicitly mentioned in the JD that is MISSING
  or only has equivalent/adjacent experience (not the exact tool), deduct 10-15 points.
- For each REQUIRED skill that is present with proven hands-on experience, no deduction.
- Bonus skills (mentioned as "Bonus" in JD) can add up to 5 points total if present.
- Do not round up generously. Be strict — most candidates should NOT score above 75
  unless they match nearly every required tool exactly.

Return ONLY valid JSON, no markdown, no code fences:
{{"score": <integer 0-100>, "reason": "<2 sentences: what matches, what's missing>", "name": "<candidate name if found, else Unknown>"}}"""
            )

            chain = prompt | llm | StrOutputParser()

            try:
                result = chain.invoke({
                    "job_description": job_description,
                    "resume_text": resume_text
                })

                cleaned = result.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.strip("`")
                    cleaned = cleaned.replace("json", "", 1).strip()

                data = json.loads(cleaned)
                score = int(data.get("score", 0))
                name = data.get("name", "Unknown")
                reason = data.get("reason", "No reasoning provided")

                if score >= 75:
                    badge_class = "score-high"
                elif score >= 50:
                    badge_class = "score-mid"
                else:
                    badge_class = "score-low"

                st.markdown(f"""
                    <div class="result-card">
                        <div class="result-name">{name}</div>
                        <div class="score-badge {badge_class}">{score}/100</div>
                        <div class="reason-label">Reasoning</div>
                        <div class="reason-text">{reason}</div>
                    </div>
                """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Model returned non-JSON. Raw output below:")
                st.code(result)
            except Exception as e:
                st.error(f"API call failed: {e}")