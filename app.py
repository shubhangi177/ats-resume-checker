import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.1-flash-lite")

# Set page config
st.set_page_config(page_title="Resume Cabin", page_icon=":robot:", layout="wide")

# Background image and style
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #002b2f;
background-image: url("https://cdn.creativefabrica.com/2022/01/25/Grainy-Gradient-Texture-Background-Graphics-24101267-1.jpg");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
visibility: hidden;
}

h1 {
color: #ffffff;
text-align: center;
font-family: monospace, sans-serif !important;
font-size: 3em;
}

h2, h3, h4 {
color: #ffffff;
font-family: monospace, sans-serif !important;
}

p, label {
color: #dcdcdc;
font-family: Arial, sans-serif !important;
font-size: 10px;
}


button {
background-color: #28a745;
color: #ffffff;
border-radius: 5px;
padding: 10px 20px;
font-size: 1.2em;
border: none;
}

button:hover {
background-color: #218838;
}

textarea, .stFileUploader {
background-color: white;
color: black;
border: 1px solid #555555;
}

.st-bd {
background-color: #28a745;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description
st.title("Resume Check: Instantly Check Your Resume!")
st.write("")

# Job Description input
st.subheader("Paste the Job Description")
jd = st.text_area("", height=200, width=800)

# Resume upload
st.subheader("Upload Your Resume")
uploaded_file = st.file_uploader("", type="pdf", help="Please upload the PDF", width=400)

# Submit button
submit = st.button("Check ATS Score")

# Processing the input
if submit:
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        extracted_text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            extracted_text += page.extract_text()

        # Generating response using the model
        input_prompt = f"""
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in the tech industry, including but not limited to [insert specific field here, e.g., software engineering, data science, data analysis, big data engineering]. Your primary task is to meticulously evaluate resumes based on the provided job description. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        Responsibilities:

        1. Assess resumes with a high degree of accuracy against the job description.
        2. Identify and highlight missing keywords crucial for the role.
        3. Provide a percentage match score reflecting the resume's alignment with the job requirements on the scale of 1-100.
        4. Offer detailed feedback for improvement to help candidates stand out.
        5. Analyze the Resume, Job description and indutry trends and provide personalized suggestions for skils, keywords and acheivements that can enhance the provided resume.
        6. Provide the suggestions for improving the language, tone and clarity of the resume content.
        7. Provide users with insights into the performance of thier resumes. Track the metrices such as - a) Application Success rates b) Views c) engagement. offers valuable feedback to improve the candidate's chances in the job market use your trained knowledge of gemini trained data . Provide  a application success rate on the scale of 1-100.

        after everytime whenever a usr refersh a page, if the provided job decription and resume is same, then always give same result. 
        

        Field-Specific Customizations:

        Software Engineering:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in software engineering. Your primary task is to meticulously evaluate resumes based on the provided job description for software engineering roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        Data Science:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in data science. Your primary task is to meticulously evaluate resumes based on the provided job description for data science roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        Data Analysis:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in data analysis. Your primary task is to meticulously evaluate resumes based on the provided job description for data analysis roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        Big Data Engineering:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in big data engineering. Your primary task is to meticulously evaluate resumes based on the provided job description for big data engineering roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        AI / MLEngineering:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in AI/ML engineering. Your primary task is to meticulously evaluate resumes based on the provided job description for AI / ML engineering roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        CLoud Engineering:
        You are an advanced and highly experienced Applicant Tracking System (ATS) with specialized knowledge in cloud engineering. Your primary task is to meticulously evaluate resumes based on the provided job description for cloud engineering roles. Considering the highly competitive job market, your goal is to offer the best possible guidance for enhancing resumes.

        Resume: {extracted_text}
        Description: {jd}

        I want the only response in 4 sectors as follows:
        • Job Description Match: \n\n
        • Missing Keywords: \n\n
        • Profile Summary: \n\n
        • Personalized suggestions for skils, keywords and acheivements that can enhance the provided resume: \n\n
        • Application Success rates : \n\n

        """

        response = model.generate_content(input_prompt)
        st.subheader("Analysis Result")
        st.write(response.text)
    else:
        st.error("Please upload a resume to continue.")
