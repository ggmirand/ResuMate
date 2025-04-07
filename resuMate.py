"""
ResuMate: AI-Powered Resume Analyzer
-------------------------------------

ResuMate is a Streamlit web app designed to help job seekers optimize their resumes 
by comparing them directly to a job description. By leveraging OpenAI's language models, 
the app generates tailored feedback to improve alignment between a resume and the requirements 
of a given job posting.

Key Features:
- Upload a resume in PDF format
- Paste a job description
- Receive AI-generated insights to improve resume-job alignment
- Simple reset functionality for ease of reuse
- Clean, minimal UI with personal branding links

Ideal for:
- Job seekers refining resumes for specific roles
- Career coaches assisting clients with job readiness
- Students and professionals seeking to break into competitive industries

All API keys are securely managed via environment variables and excluded from version control 
to protect user data and credentials.
"""

import os
import openai
import streamlit as st
import PyPDF2
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Make sure it's in a .env file under OPENAI_API_KEY.")

# Set up OpenAI client
client = openai.OpenAI(api_key=api_key)

# Helper: Extract text from uploaded PDF
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()

# Helper: Call OpenAI API to compare resume and job description
def get_feedback(resume, job):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for resume review."},
            {"role": "user", "content": f"Here's the resume:\n{resume}\n\nAnd here's the job description:\n{job}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Set up session state
if "resume_file" not in st.session_state:
    st.session_state.resume_file = None

if "job_text" not in st.session_state:
    st.session_state.job_text = ""

if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# Reset all inputs
def reset_inputs():
    st.session_state.resume_file = None
    st.session_state.job_text = ""
    st.session_state.reset_flag = not st.session_state.reset_flag
    st.rerun()

# UI
st.title("ResuMate: Resume vs Job Description")

st.write("Upload your resume and paste a job description below. We'll give you tailored feedback to help you improve your chances.")

upload_key = "resume_" + str(st.session_state.reset_flag)
file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key=upload_key)

if file:
    st.session_state.resume_file = file

desc_key = "desc_" + str(st.session_state.reset_flag)
job_input = st.text_area("Job Description", value=st.session_state.job_text, key=desc_key)
st.session_state.job_text = job_input

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Analyze"):
        if st.session_state.resume_file and st.session_state.job_text.strip():
            with st.spinner("Working on it..."):
                resume_text = read_pdf(st.session_state.resume_file)
                feedback = get_feedback(resume_text, st.session_state.job_text)
                st.success("Done!")
                st.markdown("### Feedback")
                st.write(feedback)
        else:
            st.warning("Upload a resume and enter a job description before analyzing.")
with col2:
    if st.button("Reset"):
        reset_inputs()

st.divider()

# Footer
st.markdown("Made with ❤️ by Gericho Miranda")
st.markdown("[LinkedIn](https://www.linkedin.com/in/gericho-miranda/) • [GitHub](https://github.com/GerichoMiranda)")
