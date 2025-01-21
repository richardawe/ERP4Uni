import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="Academic Management - ERP4Uni",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Academic Management")

# Tabs for different academic functions
tabs = st.tabs(["Courses", "Faculty", "Departments", "Timetable"])

# Courses Tab
with tabs[0]:
    st.header("Course Management")
    
    # Course Search and Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search Courses")
    with col2:
        department = st.selectbox("Department", ["All", "Computer Science", "Engineering", "Business"])
    
    # Sample course data (would be fetched from Django backend)
    courses_data = {
        "Course Code": ["CS101", "ENG201", "BUS301"],
        "Course Name": ["Introduction to Programming", "Circuit Analysis", "Business Ethics"],
        "Department": ["Computer Science", "Engineering", "Business"],
        "Credits": [3, 4, 3],
        "Instructor": ["Dr. Smith", "Prof. Johnson", "Dr. Williams"]
    }
    
    courses_df = pd.DataFrame(courses_data)
    st.dataframe(courses_df, use_container_width=True)
    
    # Add New Course
    st.subheader("Add New Course")
    with st.form("new_course_form"):
        course_code = st.text_input("Course Code")
        course_name = st.text_input("Course Name")
        course_dept = st.selectbox("Select Department", ["Computer Science", "Engineering", "Business"])
        credits = st.number_input("Credits", min_value=1, max_value=6)
        instructor = st.selectbox("Select Instructor", ["Dr. Smith", "Prof. Johnson", "Dr. Williams"])
        
        submit = st.form_submit_button("Add Course")
        if submit:
            st.success(f"Course {course_code} added successfully!")

# Faculty Tab
with tabs[1]:
    st.header("Faculty Management")
    
    # Faculty Directory
    faculty_data = {
        "Name": ["Dr. Smith", "Prof. Johnson", "Dr. Williams"],
        "Department": ["Computer Science", "Engineering", "Business"],
        "Position": ["Associate Professor", "Professor", "Assistant Professor"],
        "Email": ["smith@erp4uni.edu", "johnson@erp4uni.edu", "williams@erp4uni.edu"]
    }
    
    faculty_df = pd.DataFrame(faculty_data)
    st.dataframe(faculty_df, use_container_width=True)
    
    # Add New Faculty
    st.subheader("Add New Faculty")
    with st.form("new_faculty_form"):
        name = st.text_input("Full Name")
        department = st.selectbox("Department", ["Computer Science", "Engineering", "Business"])
        position = st.selectbox("Position", ["Professor", "Associate Professor", "Assistant Professor"])
        email = st.text_input("Email")
        
        submit = st.form_submit_button("Add Faculty")
        if submit:
            st.success(f"Faculty {name} added successfully!")

# Departments Tab
with tabs[2]:
    st.header("Department Management")
    
    # Department List
    dept_data = {
        "Department": ["Computer Science", "Engineering", "Business"],
        "Head": ["Dr. Smith", "Prof. Johnson", "Dr. Williams"],
        "Students": [150, 200, 180],
        "Faculty": [12, 15, 10]
    }
    
    dept_df = pd.DataFrame(dept_data)
    st.dataframe(dept_df, use_container_width=True)
    
    # Add New Department
    st.subheader("Add New Department")
    with st.form("new_department_form"):
        dept_name = st.text_input("Department Name")
        dept_head = st.selectbox("Department Head", ["Dr. Smith", "Prof. Johnson", "Dr. Williams"])
        
        submit = st.form_submit_button("Add Department")
        if submit:
            st.success(f"Department {dept_name} added successfully!")

# Timetable Tab
with tabs[3]:
    st.header("Timetable Management")
    
    # Timetable Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_dept = st.selectbox("Select Department", ["Computer Science", "Engineering", "Business"])
    with col2:
        selected_semester = st.selectbox("Select Semester", ["Fall 2024", "Spring 2025"])
    
    # Sample Timetable
    st.subheader("Weekly Schedule")
    timetable_data = {
        "Time": ["9:00 AM", "10:30 AM", "1:00 PM"],
        "Monday": ["CS101", "ENG201", "BUS301"],
        "Tuesday": ["CS102", "ENG202", "BUS302"],
        "Wednesday": ["CS101", "ENG201", "BUS301"],
        "Thursday": ["CS102", "ENG202", "BUS302"],
        "Friday": ["CS101", "ENG201", "BUS301"]
    }
    
    timetable_df = pd.DataFrame(timetable_data)
    st.dataframe(timetable_df, use_container_width=True)
    
    # Add New Schedule
    st.subheader("Add New Schedule")
    with st.form("new_schedule_form"):
        course = st.selectbox("Select Course", ["CS101", "ENG201", "BUS301"])
        day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        time = st.time_input("Select Time")
        
        submit = st.form_submit_button("Add Schedule")
        if submit:
            st.success(f"Schedule added successfully!")
