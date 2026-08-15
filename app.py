import streamlit as st
from dotenv import load_dotenv
import os 

from resume_parser import extract_resume_text, ExtractionError
from ai_analyzer import analyze_resume, AnalysisError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found, please put your api key in .env file")
    st.stop()

st.title("AI Resume Screening & Job Recommendation System")
st.write("Upload Your Resume to get your skill analysis, profile summary and job role recommendation")

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type = ['pdf', 'docx'])

if uploaded_file is not None:
    if(st.button("Analyze Resume")):
        try:
            with st.spinner("Extracting the text from resume....."):
                resume_text = extract_resume_text(uploaded_file)

            with st.spinner("Analyzing with Gemini....."):
                result = analyze_resume(resume_text, api_key)

            st.session_state['analysis_result'] = result
            st.session_state['resume_text'] = resume_text

        except ExtractionError as e:
            st.error(f"Couldn't read your resume : {e}")
        except AnalysisError as e:
            st.error(f"Analysis Failed : {e}")

if 'analysis_result' in st.session_state:
    result = st.session_state['analysis_result']

    st.divider()
    st.subheader("Profile Summary")
    st.write(result["profile_summary"])

    st.subheader("Recommended Job Role")
    st.success(result["recommended_job_role"])

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Technical Skills")
        for skill in result["technical_skills"]:
            st.markdown(f"- {skill}")
        
        st.subheader("Soft Skills")
        for skill in result["soft_skills"]:
            st.markdown(f"- {skill}")

    with col2:
        st.subheader("Missing Skills")
        st.warning("Consider building these skills for your recommended role:")
        for skill in result["missing_skills"]:
            st.markdown(f"- {skill}")


