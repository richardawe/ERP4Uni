from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Campus Life - ERP4Uni",
    page_icon="🏫",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("🏫 Campus Life")

# Create tabs for different sections
tabs = st.tabs(["Events & Activities", "Clubs & Organizations", "Sports & Recreation", "Campus Facilities"])

# Events & Activities Tab
with tabs[0]:
    st.subheader("Upcoming Events")
    
    # Event Calendar
    events_df = pd.DataFrame({
        "Event": ["Cultural Festival", "Tech Talk", "Music Concert", "Art Exhibition"],
        "Date": ["2024-02-15", "2024-02-10", "2024-02-20", "2024-02-25"],
        "Time": ["2:00 PM", "4:00 PM", "7:00 PM", "11:00 AM"],
        "Location": ["Main Hall", "Auditorium", "Amphitheater", "Art Gallery"],
        "Registration": ["Open", "Open", "Tickets Available", "Free Entry"]
    })
    st.dataframe(events_df)
    
    # Event Registration
    st.subheader("Event Registration")
    col1, col2 = st.columns(2)
    with col1:
        event = st.selectbox("Select Event", ["Cultural Festival", "Tech Talk", "Music Concert"])
        num_tickets = st.number_input("Number of Tickets", min_value=1, max_value=5, value=1)
    with col2:
        ticket_type = st.selectbox("Ticket Type", ["Student", "Faculty", "Guest"])
        special_req = st.text_input("Special Requirements")
    
    if st.button("Register for Event"):
        st.success("Event registration successful!")

# Clubs & Organizations Tab
with tabs[1]:
    st.subheader("Student Organizations")
    
    # Club Directory
    clubs_df = pd.DataFrame({
        "Club Name": ["Tech Club", "Drama Society", "Environmental Club", "Photography Club"],
        "Category": ["Academic", "Arts", "Social", "Arts"],
        "Members": [50, 30, 45, 25],
        "Status": ["Active", "Active", "Active", "Active"]
    })
    st.dataframe(clubs_df)
    
    # Club Registration
    st.subheader("Join a Club")
    col1, col2 = st.columns(2)
    with col1:
        club = st.selectbox("Select Club", ["Tech Club", "Drama Society", "Environmental Club"])
        role_interest = st.multiselect("Areas of Interest", 
            ["Member", "Event Planning", "Marketing", "Leadership"])
    with col2:
        experience = st.text_area("Relevant Experience")
    
    if st.button("Submit Application"):
        st.success("Club application submitted successfully!")
    
    # Start a New Club
    st.subheader("Start a New Club")
    col1, col2 = st.columns(2)
    with col1:
        club_name = st.text_input("Club Name")
        category = st.selectbox("Category", ["Academic", "Arts", "Social", "Sports", "Other"])
    with col2:
        description = st.text_area("Club Description")
        advisor = st.text_input("Faculty Advisor")
    
    if st.button("Submit Club Proposal"):
        st.success("Club proposal submitted for review!")

# Sports & Recreation Tab
with tabs[2]:
    st.subheader("Sports Facilities")
    
    # Facility Booking
    facilities_df = pd.DataFrame({
        "Facility": ["Basketball Court", "Tennis Court", "Swimming Pool", "Gym"],
        "Location": ["Sports Complex", "Outdoor Courts", "Aquatic Center", "Fitness Center"],
        "Hours": ["6 AM - 10 PM", "6 AM - 8 PM", "6 AM - 9 PM", "24/7"],
        "Status": ["Available", "Maintenance", "Available", "Available"]
    })
    st.dataframe(facilities_df)
    
    # Book Facility
    st.subheader("Book a Facility")
    col1, col2 = st.columns(2)
    with col1:
        facility = st.selectbox("Select Facility", ["Basketball Court", "Tennis Court", "Swimming Pool"])
        booking_date = st.date_input("Date")
    with col2:
        time_slot = st.selectbox("Time Slot", ["6:00 AM", "8:00 AM", "10:00 AM", "2:00 PM", "4:00 PM"])
        duration = st.selectbox("Duration", ["1 hour", "2 hours"])
    
    if st.button("Book Facility"):
        st.success("Facility booked successfully!")
    
    # Fitness Classes
    st.subheader("Fitness Classes")
    classes_df = pd.DataFrame({
        "Class": ["Yoga", "Zumba", "HIIT", "Swimming"],
        "Instructor": ["Sarah", "Mike", "John", "Lisa"],
        "Schedule": ["Mon/Wed 8 AM", "Tue/Thu 5 PM", "Mon/Fri 6 PM", "Tue/Thu 7 AM"],
        "Level": ["All Levels", "Beginner", "Intermediate", "All Levels"]
    })
    st.dataframe(classes_df)

# Campus Facilities Tab
with tabs[3]:
    st.subheader("Campus Facilities")
    
    # Study Spaces
    st.write("**Study Spaces**")
    study_df = pd.DataFrame({
        "Location": ["Main Library", "Student Center", "Department Labs"],
        "Available Seats": [50, 30, 20],
        "Features": ["Quiet Zone, WiFi", "Group Study, Cafe", "Computers, Printers"],
        "Hours": ["24/7", "7 AM - 11 PM", "8 AM - 10 PM"]
    })
    st.dataframe(study_df)
    
    # Dining Services
    st.write("**Dining Locations**")
    dining_df = pd.DataFrame({
        "Location": ["Main Cafeteria", "Coffee Shop", "Food Court"],
        "Cuisine": ["International", "Beverages & Snacks", "Multiple Vendors"],
        "Hours": ["7 AM - 9 PM", "6 AM - 8 PM", "10 AM - 10 PM"],
        "Payment": ["Meal Plan, Cash", "Cash, Card", "All Methods"]
    })
    st.dataframe(dining_df)
    
    # Transportation
    st.write("**Campus Transportation**")
    transport_df = pd.DataFrame({
        "Service": ["Campus Shuttle", "Bike Share", "Evening Safety Escort"],
        "Route/Location": ["Campus Loop", "Multiple Stations", "On-Demand"],
        "Schedule": ["Every 15 mins", "24/7", "6 PM - 2 AM"],
        "Status": ["Operating", "Available", "Available"]
    })
    st.dataframe(transport_df)

# Footer
st.markdown("---")
st.markdown("Need help? Contact campuslife@university.edu or visit the Student Affairs Office") 