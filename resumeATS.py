from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

def read_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config('Resume ATS')
st.header("Get your resume ATS score with feedback")
prompt = """
You are an expert in understanding resumes, named ResumeChecker. User will upload their resume and the goal is to make resume ATS score higher and person get selected for a job particular domain.  
You need to check all these following points:
0. tell what profession you think resume is good for?
1. Tell what are good points in resume.
2. Tell what can be fixed in resume with suggestions to fix.
3. Give points on following parameters: Impact, Brevity, Style, Sections, skills.
4. Tell a brief review for each section.
5. Finally give ATS score. It should be based on how good resume is out of 100 to get a job in a particular domain.
Make sure to give answers in a structured format. make sure you follow all the info
"""

upload_file = st.file_uploader("Upload PDF here", type=["pdf"])

submit_button = st.button("Get ATS Score")

if submit_button:
    pdf_text = read_pdf(upload_file)
    response = get_gemini_output(pdf_text, prompt)
    st.subheader("Here's the detailed analysis: ")
    st.write(response)
