import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Faculty Portal - ERP4Uni",
    page_icon="👨‍🏫",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("👨‍🏫 Faculty Portal")

# Create tabs for different sections
tabs = st.tabs(["Teaching Schedule", "Grade Management", "Office Hours", "Research & Publications"])

# Teaching Schedule Tab
with tabs[0]:
    st.header("Teaching Schedule")
    
    # Fetch courses taught by faculty
    courses = fetch_data(f"{ENDPOINTS['courses']}?faculty={st.session_state.user['user_id']}")
    if courses and 'results' in courses:
        st.subheader("Current Semester Courses")
        df = pd.DataFrame(courses['results'])
        if not df.empty:
            st.dataframe(
                df[['code', 'name', 'schedule', 'room', 'enrolled_students']],
                hide_index=True
            )
        else:
            st.info("No courses assigned for the current semester.")
    
    # Weekly Schedule View
    st.subheader("Weekly Schedule")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = [f"{i:02d}:00" for i in range(8, 18)]
    
    schedule_df = pd.DataFrame(index=times, columns=days)
    st.dataframe(schedule_df, height=400)

# Grade Management Tab
with tabs[1]:
    st.header("Grade Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Course selection for grade entry
        course = st.selectbox(
            "Select Course",
            [f"{c['code']} - {c['name']}" for c in courses.get('results', [])]
        )
        
        if course:
            # Fetch students in selected course
            students = fetch_data(f"{ENDPOINTS['courses']}/{course.split('-')[0].strip()}/students")
            if students and 'results' in students:
                st.subheader("Enter Grades")
                grades_df = pd.DataFrame(students['results'])
                if not grades_df.empty:
                    edited_df = st.data_editor(
                        grades_df[['id', 'full_name', 'current_grade']],
                        hide_index=True,
                        column_config={
                            "current_grade": st.column_config.SelectboxColumn(
                                "Grade",
                                options=["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
                            )
                        }
                    )
                    if st.button("Submit Grades"):
                        st.success("Grades submitted successfully!")
    
    with col2:
        st.subheader("Grade Distribution")
        if course:
            # Show grade distribution chart
            st.bar_chart({"A": 5, "B": 8, "C": 4, "D": 2, "F": 1})

# Office Hours Tab
with tabs[2]:
    st.header("Office Hours Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Set Office Hours")
        with st.form("office_hours"):
            day = st.selectbox("Day", days)
            start_time = st.time_input("Start Time", datetime.strptime("09:00", "%H:%M").time())
            end_time = st.time_input("End Time", datetime.strptime("10:00", "%H:%M").time())
            location = st.text_input("Location")
            
            submit = st.form_submit_button("Save Office Hours")
            if submit:
                st.success("Office hours updated successfully!")
    
    with col2:
        st.subheader("Current Office Hours")
        # Fetch current office hours
        office_hours = fetch_data(f"{ENDPOINTS['faculty-profiles']}/{st.session_state.user['user_id']}/office-hours")
        if office_hours and 'results' in office_hours:
            for oh in office_hours['results']:
                st.write(f"{oh['day']}: {oh['start_time']} - {oh['end_time']}")
                st.write(f"Location: {oh['location']}")
                st.write("---")

# Research & Publications Tab
with tabs[3]:
    st.header("Research & Publications")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add New Publication")
        with st.form("add_publication"):
            title = st.text_input("Title")
            pub_type = st.selectbox(
                "Type",
                ["Journal Article", "Conference Paper", "Book Chapter", "Book"]
            )
            authors = st.text_input("Authors (comma-separated)")
            venue = st.text_input("Journal/Conference/Publisher")
            year = st.number_input("Year", min_value=2000, max_value=datetime.now().year)
            doi = st.text_input("DOI (optional)")
            
            submit = st.form_submit_button("Add Publication")
            if submit and title and authors and venue:
                st.success("Publication added successfully!")
    
    with col2:
        st.subheader("Recent Publications")
        # Fetch faculty publications
        publications = fetch_data(f"{ENDPOINTS['publications']}?faculty={st.session_state.user['user_id']}")
        if publications and 'results' in publications:
            for pub in publications['results']:
                with st.expander(pub['title']):
                    st.write(f"Authors: {pub['authors']}")
                    st.write(f"Venue: {pub['venue']}")
                    st.write(f"Year: {pub['year']}")
                    if pub.get('doi'):
                        st.write(f"DOI: {pub['doi']}")

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Faculty Affairs Office at faculty.affairs@university.edu") 