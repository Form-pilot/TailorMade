import streamlit as st
import requests
from typing import Dict, Any
from config import API_URL
from models.ai_models import AIModel
from models.templates import ResumeTemplate

class ResumeApp:
    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url
        
    def call_api(self, endpoint: str, data: Dict[str, Any]) -> Dict:
        response = requests.post(f"{self.api_url}/{endpoint}", json=data)
        return response.json()
    
def main():
    st.set_page_config(page_title="Resume Tailorer", layout="wide")
    app = ResumeApp()

    st.title("Resume Tailoring Application")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Configuration")
        ai_model = st.selectbox("Select AI Model", [model.value for model in AIModel], index=0)
        resume_template = st.selectbox("Select Resume Template", [template.value for template in ResumeTemplate], index=2)
        job_description = st.text_area("Enter Job Description", height=200)
        resume = st.text_area("Enter Resume", height=200)
    tab1, tab2, tab3, tab4 = st.tabs(["Generate Resume", "Generate Cover Letter", "Answer application questions", "CV Editor"])
    
    
    job_data = {
        "profile": {"resume": {"text": resume}},
        "job": {"description": job_description},
        "tailoring_options": {
            "ai_model": ai_model,
            "resume_template": resume_template
        }
    }

    with tab1:
        if st.button("Check Eligibility"):
            result = app.call_api("determine_eligibility", job_data)
            st.write("Eligibility:", result["eligibility"])
            st.write("Reason:", result["reason"])
        
        if st.button("Check Suitability"):
            result = app.call_api("determine_suitability", job_data)
            st.write("Suitability:", result["suitability"])
            st.write("Reason:", result["reason"])
        
        if st.button("Generate Resume"):
            result = app.call_api("generate-latex-resume-save", job_data)
            st.session_state['latex_code'] = result['latex_code']
            st.success(f"Resume saved: {result['path']}")

    
    with tab2:
        if st.button("Generate Cover Letter"):
            result = app.call_api("generate-tailored-plain-coverletter", job_data)
            st.text_area("Generated Cover Letter", value=result, height=400)
    
    with tab3:
        question_description = st.text_area("Enter Question", height=200)
        # Adding the question description
        job_data["question"] = {"description": question_description}
        if st.button("Generate answer"):
            result = app.call_api("answer-application-questions", job_data)
            st.text_area("Generated Answer", value=result, height=400)
    
    with tab4:
        if 'latex_code' not in st.session_state:
            st.session_state['latex_code'] = ""
        
        st.header("LaTeX Editor")
        edited_latex = st.text_area("Edit LaTeX Code", value=st.session_state['latex_code'], height=400)
        if st.button("Save Final PDF"):
            save_data = {
                "latex_code": edited_latex,
                "tailoring_options": {
                    "ai_model":ai_model,
                    "resume_template": resume_template
                }
            }
            result = app.call_api("save-latex-resume", save_data)
            if result.get('path'):
                st.success(f"PDF saved at: {result['path']}")


if __name__ == "__main__":
    main()
