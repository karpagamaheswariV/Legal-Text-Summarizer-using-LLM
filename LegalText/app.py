import streamlit as st
import os
from dotenv import load_dotenv

# Try to import the Groq client
try:
    from groq import Groq
    _GROQ_AVAILABLE = True
except Exception:
    Groq = None
    _GROQ_AVAILABLE = False

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Page Config
st.set_page_config(
    page_title="Legal Text Summarizer",
    page_icon="⚖",
    layout="centered",
)

# Custom CSS for Beautiful UI
st.markdown("""
    <style>
        /* Main App Background */
        .stApp {
            background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e);
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Legal Text Summarizer</h1>
        <p class="main-subtitle">Transform complex legal documents into clear, understandable summaries</p>
    </div>
""", unsafe_allow_html=True)

# API Key Validation
if not API_KEY:
    st.error("GROQ_API_KEY is not set in your environment. Please add it to your .env file.")
    st.stop()

if not _GROQ_AVAILABLE:
    st.warning("Python package 'groq' is not installed. Run: pip install groq")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Main Content
legal_text = None

st.markdown('<div class="content-card fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Input Legal Text</h2>', unsafe_allow_html=True)

legal_text = st.text_area(
    "Paste your legal document here",
    height=350,
    placeholder="Paste contract clauses, legal agreements, terms of service, or any legal document you want to understand better...",
    label_visibility="collapsed"
)

if legal_text:
    char_count = len(legal_text)
    word_count = len(legal_text.split())
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <span class="stat-number">{char_count}</span>
                <span class="stat-label">Characters</span>
            </div>
            <div class="stat-box">
                <span class="stat-number">{word_count}</span>
                <span class="stat-label">Words</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)
summarize = st.button("Generate Summary")
st.markdown('</div>', unsafe_allow_html=True)

# Summarization Logic
if summarize:
    if not legal_text.strip():
        st.warning("Please paste some legal text to summarize!")
    else:
        with st.spinner("Analyzing and summarizing your text..."):
            prompt = (
                "Summarize the following legal text in very simple and clear English. "
                "Keep the meaning accurate. Avoid legal jargon. Make it easy to understand for someone without legal knowledge.\n\n"
                f"TEXT:\n{legal_text}"
            )

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                
                summary = response.choices[0].message.content
                
                # Display Result
                st.markdown('<div class="content-card fade-in-up">', unsafe_allow_html=True)
                st.markdown('<h2 class="section-header">Summary Result</h2>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-box"><p>{summary}</p></div>', unsafe_allow_html=True)
                
                st.success("Summary generated successfully!")
                
                # Download option
                st.download_button(
                    label="Download Summary as Text File",
                    data=summary,
                    file_name="legal_summary.txt",
                    mime="text/plain"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")