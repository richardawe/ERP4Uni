import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Academic Records - ERP4Uni",
    page_icon="📚",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("📚 Academic Records")

# Create tabs for different sections
tabs = st.tabs(["Course Management", "Grades", "Attendance", "Transcript Requests"])

# Course Management Tab
with tabs[0]:
    st.header("Course Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Courses")
        # Fetch courses from API
        courses = fetch_data(f"{ENDPOINTS['courses']}?semester__is_active=true")
        if courses and 'results' in courses:
            df = pd.DataFrame(courses['results'])
            if not df.empty:
                st.dataframe(
                    df[['code', 'name', 'credits', 'department__name', 'semester__name']],
                    hide_index=True
                )
            else:
                st.info("No courses found for the current semester.")
    
    with col2:
        st.subheader("Course Registration")
        with st.form("course_registration"):
            selected_courses = st.multiselect(
                "Select Courses",
                options=[f"{c['code']} - {c['name']}" for c in courses.get('results', [])]
            )
            submit = st.form_submit_button("Register")
            if submit and selected_courses:
                st.success("Course registration submitted successfully!")

# Grades Tab
with tabs[1]:
    st.header("Grade Records")
    
    # Fetch grades from API
    grades = fetch_data(f"{ENDPOINTS['courses']}?student={st.session_state.user['user_id']}")
    if grades and 'results' in grades:
        st.subheader("Current Semester Grades")
        current_grades = pd.DataFrame(grades['results'])
        if not current_grades.empty:
            st.dataframe(
                current_grades[['code', 'name', 'grade', 'status']],
                hide_index=True
            )
        else:
            st.info("No grades available for the current semester.")
        
        st.subheader("GPA Calculator")
        gpa = st.number_input("Current GPA", min_value=0.0, max_value=4.0, step=0.1)
        if st.button("Calculate Cumulative GPA"):
            st.metric("Cumulative GPA", f"{gpa:.2f}")

# Attendance Tab
with tabs[2]:
    st.header("Attendance Records")
    
    # Fetch attendance from API
    attendance = fetch_data(f"{ENDPOINTS['courses']}?student={st.session_state.user['user_id']}&attendance=true")
    if attendance and 'results' in attendance:
        st.subheader("Attendance Summary")
        att_df = pd.DataFrame(attendance['results'])
        if not att_df.empty:
            st.dataframe(
                att_df[['code', 'name', 'total_classes', 'attended', 'percentage']],
                hide_index=True
            )
        else:
            st.info("No attendance records found.")

# Transcript Requests Tab
with tabs[3]:
    st.header("Transcript Requests")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Request Official Transcript")
        with st.form("transcript_request"):
            purpose = st.selectbox(
                "Purpose of Request",
                ["Further Education", "Employment", "Personal Records", "Other"]
            )
            copies = st.number_input("Number of Copies", min_value=1, max_value=5)
            delivery = st.radio(
                "Delivery Method",
                ["Digital Copy", "Physical Copy", "Both"]
            )
            notes = st.text_area("Additional Notes")
            
            submit = st.form_submit_button("Submit Request")
            if submit:
                st.success("Transcript request submitted successfully!")
    
    with col2:
        st.subheader("Previous Requests")
        # Fetch previous requests from API
        previous_requests = fetch_data(f"{ENDPOINTS['transcript_requests']}?student={st.session_state.user['user_id']}")
        if previous_requests and 'results' in previous_requests:
            for req in previous_requests['results']:
                with st.expander(f"Request #{req['id']} - {req['status']}"):
                    st.write(f"Requested on: {req['request_date']}")
                    st.write(f"Purpose: {req['purpose']}")
                    st.write(f"Status: {req['status']}")

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Academic Affairs Office at academic.affairs@university.edu") 