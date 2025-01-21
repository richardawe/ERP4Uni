import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data

def render_application_form():
    with st.form("application_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            email = st.text_input("Email")
            dob = st.date_input("Date of Birth")
        with col2:
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone Number")
            gender = st.selectbox("Gender", ["Select...", "Male", "Female", "Other"])
        
        st.subheader("Academic Information")
        program = st.selectbox("Program", ["Select...", "Bachelor's", "Master's", "PhD"])
        department = st.selectbox("Department", ["Select...", "Computer Science", "Engineering", "Business"])
        intake = st.selectbox("Intake", ["Select...", "Fall 2025", "Spring 2026"])
        
        st.subheader("Documents")
        transcripts = st.file_uploader("Upload Transcripts", type=["pdf"])
        cv = st.file_uploader("Upload CV", type=["pdf"])
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            if all([first_name, last_name, email, phone, program != "Select...", department != "Select..."]):
                st.success("Application submitted successfully!")
            else:
                st.error("Please fill in all required fields")

def render_application_status():
    st.subheader("Application Status")
    
    # Sample data - replace with API call
    applications = pd.DataFrame({
        'Application ID': ['APP001', 'APP002'],
        'Program': ['Master's', 'PhD'],
        'Department': ['Computer Science', 'Engineering'],
        'Status': ['Under Review', 'Documents Pending'],
        'Last Updated': ['2025-01-20', '2025-01-19']
    })
    
    st.dataframe(applications)

def render_document_upload():
    st.subheader("Document Upload")
    
    doc_type = st.selectbox("Document Type", [
        "Academic Transcripts",
        "Letters of Recommendation",
        "Statement of Purpose",
        "English Proficiency Test",
        "Identity Document"
    ])
    
    uploaded_file = st.file_uploader(f"Upload {doc_type}", type=["pdf", "jpg", "png"])
    if uploaded_file:
        st.success(f"{doc_type} uploaded successfully!")

# Main page content
st.title("📝 Applications & Admissions")

# Create tabs for different functions
tabs = st.tabs(["New Application", "Application Status", "Document Upload"])

with tabs[0]:
    render_application_form()

with tabs[1]:
    render_application_status()

with tabs[2]:
    render_document_upload() 