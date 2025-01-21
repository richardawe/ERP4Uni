import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data

def render_library():
    st.subheader("Library Services")
    
    # Search catalog
    st.subheader("Library Catalog")
    search = st.text_input("Search Books, Journals, and Resources")
    format_filter = st.multiselect(
        "Resource Type",
        ["Books", "E-Books", "Journals", "Articles", "Multimedia"]
    )
    
    # Sample search results
    if search:
        results = pd.DataFrame({
            'Title': ['Introduction to Data Science', 'Machine Learning Basics', 'Python Programming'],
            'Author': ['John Smith', 'Jane Doe', 'Bob Johnson'],
            'Type': ['Book', 'E-Book', 'Book'],
            'Status': ['Available', 'Available', 'Checked Out'],
            'Location': ['Main Library', 'Online', 'Main Library']
        })
        st.dataframe(results)
    
    # Borrowed items
    st.subheader("My Borrowed Items")
    borrowed = pd.DataFrame({
        'Title': ['Database Systems', 'AI Fundamentals'],
        'Due Date': ['2025-02-15', '2025-02-01'],
        'Status': ['Due Soon', 'Overdue'],
        'Renewals Left': [2, 0]
    })
    st.dataframe(borrowed)
    
    # Room booking
    st.subheader("Study Room Booking")
    with st.form("room_booking"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
            start_time = st.time_input("Start Time")
        with col2:
            room_type = st.selectbox("Room Type", ["Individual Study", "Group Study", "Media Room"])
            duration = st.slider("Duration (hours)", 1, 4, 2)
        
        submitted = st.form_submit_button("Book Room")
        if submitted:
            st.success("Room booked successfully!")

def render_housing():
    st.subheader("Housing Services")
    
    # Housing status
    status = st.selectbox(
        "Current Housing Status",
        ["Not Applied", "Application Submitted", "Room Assigned", "Checked In"]
    )
    
    # Available housing
    st.subheader("Available Housing Options")
    housing = pd.DataFrame({
        'Building': ['North Hall', 'South Hall', 'West Hall'],
        'Room Type': ['Single', 'Double', 'Suite'],
        'Semester Fee': ['$3,000', '$2,500', '$3,500'],
        'Availability': ['Available', 'Limited', 'Waitlist']
    })
    st.dataframe(housing)
    
    # Housing application
    st.subheader("Housing Application")
    with st.form("housing_application"):
        preferred_building = st.selectbox("Preferred Building", housing['Building'])
        room_type = st.selectbox("Room Type", ["Single", "Double", "Suite"])
        roommate_preference = st.text_input("Preferred Roommate (if any)")
        special_requests = st.text_area("Special Requests/Accommodations")
        
        col1, col2 = st.columns(2)
        with col1:
            move_in = st.date_input("Move-in Date")
        with col2:
            term = st.selectbox("Term", ["Spring 2025", "Fall 2025"])
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            st.success("Housing application submitted successfully!")

def render_wellness():
    st.subheader("Wellness Services")
    
    # Service categories
    service_type = st.selectbox(
        "Service Category",
        ["Counseling Services", "Health Center", "Fitness & Recreation"]
    )
    
    if service_type == "Counseling Services":
        # Counseling appointment booking
        st.subheader("Book Counseling Session")
        with st.form("counseling_booking"):
            counselor = st.selectbox(
                "Select Counselor",
                ["Dr. Smith - General Counseling", "Dr. Johnson - Academic Counseling", "Dr. Brown - Career Counseling"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Preferred Date")
            with col2:
                time = st.selectbox("Preferred Time", ["9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM"])
            
            session_type = st.radio("Session Type", ["In-person", "Virtual"])
            reason = st.text_area("Reason for Visit")
            
            submitted = st.form_submit_button("Book Session")
            if submitted:
                st.success("Counseling session booked successfully!")
    
    elif service_type == "Health Center":
        # Health center services
        st.subheader("Health Center Services")
        services = [
            "General Check-up",
            "Vaccination",
            "Laboratory Tests",
            "Prescription Refill",
            "Specialist Referral"
        ]
        for service in services:
            if st.button(service):
                st.info(f"Book an appointment for {service}")
        
        # Health records
        st.subheader("My Health Records")
        with st.expander("Vaccination Records"):
            st.write("• COVID-19 Vaccination - Complete")
            st.write("• Flu Shot - Due")
        with st.expander("Recent Visits"):
            st.write("• General Check-up (2024-12-15)")
            st.write("• Flu Shot (2024-10-01)")
    
    else:  # Fitness & Recreation
        # Fitness facilities
        st.subheader("Fitness & Recreation")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Gym Status", "Open")
            st.metric("Pool Status", "Open")
        with col2:
            st.metric("Current Gym Capacity", "65%")
            st.metric("Pool Lanes Available", "4")
        
        # Class registration
        st.subheader("Fitness Classes")
        classes = pd.DataFrame({
            'Class': ['Yoga', 'Swimming', 'HIIT', 'Basketball'],
            'Schedule': ['Mon/Wed 9:00 AM', 'Tue/Thu 2:00 PM', 'Fri 4:00 PM', 'Sat 10:00 AM'],
            'Instructor': ['Sarah', 'Mike', 'Lisa', 'John'],
            'Spots Left': [5, 8, 3, 10]
        })
        st.dataframe(classes)
        
        # Equipment booking
        st.subheader("Equipment Booking")
        with st.form("equipment_booking"):
            equipment = st.selectbox(
                "Select Equipment",
                ["Basketball", "Tennis Racket", "Badminton Set", "Table Tennis"]
            )
            duration = st.slider("Duration (hours)", 1, 3, 1)
            submitted = st.form_submit_button("Book Equipment")
            if submitted:
                st.success("Equipment booked successfully!")

# Main page content
st.title("🎯 Student Support Services")

# Create tabs for different functions
tabs = st.tabs(["Library", "Housing", "Wellness"])

with tabs[0]:
    render_library()

with tabs[1]:
    render_housing()

with tabs[2]:
    render_wellness() 