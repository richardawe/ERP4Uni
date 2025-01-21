from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Student Support - ERP4Uni",
    page_icon="🎯",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("🎯 Student Support")

# Create tabs for different sections
tabs = st.tabs(["Counseling Services", "Health Services", "Career Development", "Academic Support"])

# Counseling Services Tab
with tabs[0]:
    st.subheader("Schedule Counseling Session")
    
    col1, col2 = st.columns(2)
    with col1:
        counselor = st.selectbox("Select Counselor", 
            ["Dr. Sarah Smith - Academic", "Dr. John Doe - Career", "Dr. Jane Wilson - Personal"])
        session_date = st.date_input("Preferred Date")
    with col2:
        session_type = st.selectbox("Session Type", ["In-person", "Virtual"])
        time_slot = st.selectbox("Time Slot", 
            ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"])
    
    reason = st.text_area("Reason for Visit (Optional)")
    if st.button("Schedule Appointment"):
        st.success("Counseling session scheduled successfully!")
    
    st.subheader("My Appointments")
    appointments_df = pd.DataFrame({
        "Date": ["2024-02-01", "2024-01-15"],
        "Counselor": ["Dr. Sarah Smith", "Dr. John Doe"],
        "Type": ["Academic", "Career"],
        "Status": ["Scheduled", "Completed"]
    })
    st.dataframe(appointments_df)

# Health Services Tab
with tabs[1]:
    st.subheader("Health Services")
    
    # Quick Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🏥 Emergency Contact**\n911 for emergencies\nHealth Center: (555) 123-4567")
    with col2:
        st.info("**⏰ Hours of Operation**\nMon-Fri: 8:00 AM - 6:00 PM\nSat: 9:00 AM - 1:00 PM")
    with col3:
        st.info("**🚑 After Hours**\nCall: (555) 123-4567\nUrgent Care: 123 Medical Ave")
    
    st.subheader("Schedule Medical Appointment")
    col1, col2 = st.columns(2)
    with col1:
        service_type = st.selectbox("Service Type", 
            ["General Checkup", "Vaccination", "Mental Health", "Physical Therapy"])
        appt_date = st.date_input("Appointment Date", key="health_date")
    with col2:
        provider = st.selectbox("Healthcare Provider", 
            ["Dr. Williams - General", "Dr. Brown - Mental Health", "Dr. Davis - Physical Therapy"])
        appt_time = st.selectbox("Appointment Time", 
            ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM"])
    
    symptoms = st.text_area("Symptoms/Notes")
    if st.button("Book Appointment"):
        st.success("Medical appointment scheduled successfully!")
    
    st.subheader("Health Records")
    records_df = pd.DataFrame({
        "Date": ["2024-01-15", "2023-12-01"],
        "Type": ["General Checkup", "Vaccination"],
        "Provider": ["Dr. Williams", "Dr. Brown"],
        "Notes": ["Regular checkup", "COVID-19 Booster"]
    })
    st.dataframe(records_df)

# Career Development Tab
with tabs[2]:
    st.subheader("Career Services")
    
    # Career Resources
    st.write("**Available Resources**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resume Reviews", "Available")
        st.metric("Mock Interviews", "3 slots")
    with col2:
        st.metric("Career Workshops", "2 upcoming")
        st.metric("Job Postings", "150+")
    
    # Job Board
    st.subheader("Job Board")
    jobs_df = pd.DataFrame({
        "Position": ["Software Engineer", "Data Analyst", "Research Assistant"],
        "Company": ["Tech Corp", "Analytics Inc", "Research Lab"],
        "Location": ["New York", "Remote", "Boston"],
        "Type": ["Full-time", "Full-time", "Part-time"]
    })
    st.dataframe(jobs_df)
    
    # Career Events
    st.subheader("Upcoming Career Events")
    events_df = pd.DataFrame({
        "Event": ["Career Fair", "Resume Workshop", "Industry Panel"],
        "Date": ["2024-02-15", "2024-02-01", "2024-02-10"],
        "Location": ["Main Hall", "Room 201", "Auditorium"],
        "Registration": ["Open", "Open", "Closed"]
    })
    st.dataframe(events_df)
    
    # Schedule Career Counseling
    st.subheader("Schedule Career Counseling")
    col1, col2 = st.columns(2)
    with col1:
        career_service = st.selectbox("Service Type", 
            ["Resume Review", "Mock Interview", "Career Planning", "Job Search Strategy"])
        career_date = st.date_input("Preferred Date", key="career_date")
    with col2:
        career_time = st.selectbox("Preferred Time", 
            ["10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM"])
        format_pref = st.selectbox("Format", ["In-person", "Virtual"])
    
    if st.button("Schedule Session"):
        st.success("Career counseling session scheduled successfully!")

# Academic Support Tab
with tabs[3]:
    st.subheader("Academic Support Services")
    
    # Tutoring Services
    st.write("**Available Tutoring Services**")
    tutoring_df = pd.DataFrame({
        "Subject": ["Mathematics", "Physics", "Computer Science"],
        "Tutor": ["John Smith", "Alice Johnson", "Mike Brown"],
        "Availability": ["Mon/Wed", "Tue/Thu", "Wed/Fri"],
        "Format": ["In-person", "Virtual", "Both"]
    })
    st.dataframe(tutoring_df)
    
    # Schedule Tutoring
    st.subheader("Schedule Tutoring Session")
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject", ["Mathematics", "Physics", "Computer Science"])
        tutor = st.selectbox("Tutor", ["John Smith", "Alice Johnson", "Mike Brown"])
    with col2:
        session_date = st.date_input("Session Date", key="tutor_date")
        session_time = st.selectbox("Session Time", 
            ["09:00 AM", "10:00 AM", "02:00 PM", "03:00 PM"])
    
    topics = st.text_area("Topics to Cover")
    if st.button("Book Tutoring Session"):
        st.success("Tutoring session booked successfully!")

# Footer
st.markdown("---")
st.markdown("Need help? Contact studentsupport@university.edu or visit the Student Support Center") 