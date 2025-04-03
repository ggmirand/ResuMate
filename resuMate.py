import openai
import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("API key not found. Make sure you have an .env file with OPENAI_API_KEY set.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = "".join([page.extract_text() + "\n" for page in pdf_reader.pages])
    return text.strip()

# Function to analyze resume against a job description
def analyze_resume(resume_text, job_description):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Analyze this resume against a job description."},
            {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Initialize session state variables if they don't exist
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "uploaded_resume" not in st.session_state:
    st.session_state.uploaded_resume = None  # Track uploaded file

if "clear_trigger" not in st.session_state:
    st.session_state.clear_trigger = False  # Flag to reset inputs

# Function to reset everything
def reset_all():
    st.session_state.job_description = ""  # Clear job description
    st.session_state.uploaded_resume = None  # Remove file reference
    st.session_state.clear_trigger = not st.session_state.clear_trigger  # Toggle to refresh widgets
    st.rerun()  # Force UI refresh

# Streamlit UI
st.title("📄 ResuMate: AI Resume Analyzer")

st.subheader("Upload Your Resume (PDF)")

# Reset file uploader by using a dynamic key
upload_key = "uploader_" + str(st.session_state.clear_trigger)  # New key forces re-render
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key=upload_key)

# Store file in session state
if uploaded_file is not None:
    st.session_state.uploaded_resume = uploaded_file

st.subheader("Paste the Job Description")

# 🔥 Dynamic key to force text input refresh
job_desc_key = "job_desc_" + str(st.session_state.clear_trigger)
job_description = st.text_area("Paste job description:", value=st.session_state.job_description, key=job_desc_key)

# Update session state when user types
st.session_state.job_description = job_description

# Full reset button (clears everything)
if st.button("Reset All"):
    reset_all()

# Analyze resume
if st.button("Analyze Resume"):
    if st.session_state.uploaded_resume and st.session_state.job_description.strip():
        with st.spinner("Analyzing... ⏳"):
            resume_text = extract_text_from_pdf(st.session_state.uploaded_resume)
            feedback = analyze_resume(resume_text, st.session_state.job_description)
            st.success("✅ Analysis Complete!")
            st.subheader("💡 AI Feedback")
            st.write(feedback)
    else:
        st.error("⚠️ Please upload a resume and paste a job description.")


# Add LinkedIn and GitHub links
st.markdown("### 🌐 Connect with Me")
st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/gericho-miranda/)")
st.markdown("[💻 GitHub](https://github.com/GerichoMiranda)")
