from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Faculty Portal - ERP4Uni",
    page_icon="👨‍🏫",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("👨‍🏫 Faculty Portal")

# Create tabs for different sections
tabs = st.tabs(["Teaching Schedule", "Grade Management", "Office Hours", "Research & Publications"])

# Teaching Schedule Tab
with tabs[0]:
    st.subheader("Current Teaching Schedule")
    schedule_df = pd.DataFrame({
        "Course Code": ["CS101", "CS301", "CS401"],
        "Course Name": ["Introduction to Programming", "Database Systems", "Advanced AI"],
        "Schedule": ["Mon/Wed 10:00-11:30", "Tue/Thu 14:00-15:30", "Fri 09:00-12:00"],
        "Room": ["Room 101", "Lab 203", "Room 405"],
        "Enrolled": [45, 35, 25]
    })
    st.dataframe(schedule_df)
    
    st.subheader("Course Materials")
    col1, col2 = st.columns(2)
    with col1:
        course = st.selectbox("Select Course", ["CS101", "CS301", "CS401"])
        material_type = st.selectbox("Material Type", ["Lecture Notes", "Assignments", "Exams"])
    with col2:
        uploaded_file = st.file_uploader("Upload Material")
        if st.button("Upload"):
            st.success("Material uploaded successfully!")

# Grade Management Tab
with tabs[1]:
    st.subheader("Grade Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        grade_course = st.selectbox("Course", ["CS101", "CS301", "CS401"], key="grade_course")
        assessment = st.selectbox("Assessment", ["Assignment 1", "Midterm", "Final Exam"])
    with col2:
        upload_grades = st.file_uploader("Upload Grades (CSV)")
        if st.button("Import Grades"):
            st.success("Grades imported successfully!")
    
    st.subheader("Grade Distribution")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Class Average", "85%")
        st.metric("Passing Rate", "92%")
    with col4:
        st.metric("Highest Grade", "98%")
        st.metric("Lowest Grade", "65%")

# Office Hours Tab
with tabs[2]:
    st.subheader("Office Hours Schedule")
    
    col1, col2 = st.columns(2)
    with col1:
        day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        start_time = st.time_input("Start Time", datetime.strptime("09:00", "%H:%M").time())
    with col2:
        location = st.selectbox("Location", ["Office 405", "Online (Zoom)", "Department Library"])
        end_time = st.time_input("End Time", datetime.strptime("10:00", "%H:%M").time())
    
    if st.button("Add Office Hours"):
        st.success("Office hours added successfully!")
    
    st.subheader("Current Office Hours")
    office_hours_df = pd.DataFrame({
        "Day": ["Monday", "Wednesday", "Thursday"],
        "Time": ["09:00-10:00", "14:00-15:00", "11:00-12:00"],
        "Location": ["Office 405", "Online (Zoom)", "Department Library"],
        "Status": ["Available", "Available", "Available"]
    })
    st.dataframe(office_hours_df)

# Research & Publications Tab
with tabs[3]:
    st.subheader("Research Projects")
    projects_df = pd.DataFrame({
        "Project": ["AI in Education", "Database Optimization", "Cloud Computing"],
        "Role": ["Principal Investigator", "Co-Investigator", "Research Lead"],
        "Status": ["Active", "Completed", "Planning"],
        "Funding": ["$50,000", "$30,000", "Pending"]
    })
    st.dataframe(projects_df)
    
    st.subheader("Recent Publications")
    publications_df = pd.DataFrame({
        "Title": ["Machine Learning in Higher Education", "Cloud Database Performance", "AI Ethics"],
        "Journal": ["Education Technology", "Database Journal", "AI Review"],
        "Date": ["2024", "2023", "2023"],
        "Citations": [12, 25, 18]
    })
    st.dataframe(publications_df)
    
    st.subheader("Add New Publication")
    col1, col2 = st.columns(2)
    with col1:
        pub_title = st.text_input("Publication Title")
        journal = st.text_input("Journal/Conference")
    with col2:
        pub_date = st.date_input("Publication Date")
        doi = st.text_input("DOI")
    
    if st.button("Add Publication"):
        st.success("Publication added successfully!")

# Footer
st.markdown("---")
st.markdown("Need help? Contact faculty.support@university.edu or visit the Faculty Affairs Office") 