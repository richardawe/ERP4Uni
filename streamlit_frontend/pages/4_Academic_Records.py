from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Academic Records - ERP4Uni",
    page_icon="📚",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("📚 Academic Records")

# Create tabs for different sections
tabs = st.tabs(["Course Management", "Grades", "Attendance", "Transcript Requests"])

# Course Management Tab
with tabs[0]:
    st.subheader("Current Courses")
    courses_df = pd.DataFrame({
        "Course Code": ["CS101", "MATH201", "PHY301"],
        "Course Name": ["Introduction to Programming", "Advanced Calculus", "Modern Physics"],
        "Credits": [3, 4, 4],
        "Instructor": ["Dr. Smith", "Dr. Johnson", "Dr. Brown"],
        "Schedule": ["Mon/Wed 10:00-11:30", "Tue/Thu 14:00-15:30", "Mon/Wed 14:00-15:30"]
    })
    st.dataframe(courses_df)
    
    st.subheader("Course Registration")
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics"])
        course_level = st.selectbox("Course Level", ["100 - Introductory", "200 - Intermediate", "300 - Advanced"])
    with col2:
        time_preference = st.multiselect("Preferred Time Slots", 
            ["Morning (8:00-12:00)", "Afternoon (12:00-17:00)", "Evening (17:00-21:00)"])
    
    if st.button("Search Available Courses"):
        st.dataframe({
            "Course Code": ["CS102", "CS201"],
            "Course Name": ["Web Development", "Data Structures"],
            "Credits": [3, 4],
            "Available Seats": [15, 8],
            "Schedule": ["Tue/Thu 11:00-12:30", "Mon/Wed 15:00-16:30"]
        })

# Grades Tab
with tabs[1]:
    st.subheader("Current Semester Grades")
    grades_df = pd.DataFrame({
        "Course": ["CS101", "MATH201", "PHY301"],
        "Assignment": ["85%", "92%", "88%"],
        "Midterm": ["78%", "85%", "90%"],
        "Final": ["Pending", "Pending", "Pending"],
        "Current Grade": ["B+", "A-", "A"]
    })
    st.dataframe(grades_df)
    
    st.subheader("GPA Calculator")
    col1, col2 = st.columns(2)
    with col1:
        credits = st.number_input("Course Credits", min_value=1, max_value=5, value=3)
        grade = st.selectbox("Expected Grade", ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"])
    with col2:
        st.metric("Current GPA", "3.75")
        st.metric("Projected GPA", "3.80")

# Attendance Tab
with tabs[2]:
    st.subheader("Attendance Records")
    attendance_df = pd.DataFrame({
        "Course": ["CS101", "MATH201", "PHY301"],
        "Total Classes": [28, 26, 27],
        "Attended": [26, 24, 25],
        "Percentage": ["92.8%", "92.3%", "92.6%"],
        "Status": ["Good", "Good", "Good"]
    })
    st.dataframe(attendance_df)
    
    st.info("Minimum attendance required: 75%")

# Transcript Requests Tab
with tabs[3]:
    st.subheader("Request Official Transcript")
    
    col1, col2 = st.columns(2)
    with col1:
        transcript_type = st.selectbox("Transcript Type", ["Official", "Unofficial"])
        delivery_method = st.selectbox("Delivery Method", ["Electronic", "Mail"])
    with col2:
        copies = st.number_input("Number of Copies", min_value=1, max_value=5, value=1)
        urgent = st.checkbox("Urgent Processing (Additional Fee Applies)")
    
    recipient_info = st.text_area("Recipient Information (if different from student)")
    if st.button("Submit Request"):
        st.success("Transcript request submitted successfully!")
    
    st.subheader("Previous Requests")
    requests_df = pd.DataFrame({
        "Request Date": ["2024-01-15", "2023-12-01"],
        "Type": ["Official", "Unofficial"],
        "Status": ["Processing", "Completed"],
        "Tracking": ["TR123456", "TR123455"]
    })
    st.dataframe(requests_df)

# Footer
st.markdown("---")
st.markdown("Need help? Contact registrar@university.edu or visit the Registrar's Office") 