import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Housing Management - ERP4Uni",
    page_icon="🏠",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("🏠 Housing Management")

# Create tabs for different sections
tabs = st.tabs(["Housing Overview", "Room Selection", "Maintenance", "Housing Applications"])

# Housing Overview Tab
with tabs[0]:
    st.header("Housing Overview")
    
    # Housing Statistics
    col1, col2, col3 = st.columns(3)
    
    # Fetch housing stats from API
    housing_stats = fetch_data(f"{ENDPOINTS['housing']}/stats")
    if housing_stats:
        with col1:
            st.metric("Total Capacity", housing_stats.get('total_capacity', 0))
            st.metric("Occupied Rooms", housing_stats.get('occupied_rooms', 0))
        with col2:
            st.metric("Available Rooms", housing_stats.get('available_rooms', 0))
            st.metric("Maintenance Requests", housing_stats.get('maintenance_requests', 0))
        with col3:
            st.metric("Occupancy Rate", f"{housing_stats.get('occupancy_rate', 0)}%")
            st.metric("Average Rating", f"{housing_stats.get('avg_rating', 0)}/5")
    
    # Building Status
    st.subheader("Building Status")
    buildings = fetch_data(f"{ENDPOINTS['housing']}/buildings")
    if buildings and 'results' in buildings:
        for building in buildings['results']:
            with st.expander(f"{building['name']} - {building['type']}"):
                col4, col5 = st.columns(2)
                with col4:
                    st.write(f"**Total Rooms:** {building['total_rooms']}")
                    st.write(f"**Available:** {building['available_rooms']}")
                    st.write(f"**Amenities:** {', '.join(building['amenities'])}")
                with col5:
                    st.metric("Occupancy", f"{building['occupancy_rate']}%")
                    st.progress(building['occupancy_rate'] / 100)

# Room Selection Tab
with tabs[1]:
    st.header("Room Selection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Room Search
        st.subheader("Search Available Rooms")
        with st.form("room_search"):
            building = st.selectbox(
                "Building",
                ["All Buildings", "North Hall", "South Hall", "East Hall", "West Hall"]
            )
            room_type = st.selectbox(
                "Room Type",
                ["Any", "Single", "Double", "Suite", "Apartment"]
            )
            max_price = st.slider(
                "Maximum Price per Semester",
                min_value=1000,
                max_value=5000,
                value=3000,
                step=100
            )
            
            submit = st.form_submit_button("Search Rooms")
            if submit:
                # Display search results
                rooms = fetch_data(f"{ENDPOINTS['housing']}/rooms")
                if rooms and 'results' in rooms:
                    st.dataframe(
                        pd.DataFrame(rooms['results'])[
                            ['building', 'room_number', 'type', 'price', 'availability']
                        ],
                        hide_index=True
                    )
    
    with col2:
        st.subheader("My Room")
        current_room = fetch_data(f"{ENDPOINTS['housing']}/my-room")
        if current_room:
            st.info(f"""
            **Building:** {current_room.get('building', 'N/A')}
            **Room:** {current_room.get('room_number', 'N/A')}
            **Type:** {current_room.get('type', 'N/A')}
            **Move-in Date:** {current_room.get('move_in_date', 'N/A')}
            """)

# Maintenance Tab
with tabs[2]:
    st.header("Maintenance")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Submit Maintenance Request")
        with st.form("maintenance_request"):
            request_type = st.selectbox(
                "Request Type",
                ["Plumbing", "Electrical", "HVAC", "Furniture", "Cleaning", "Other"]
            )
            priority = st.select_slider(
                "Priority",
                options=["Low", "Medium", "High", "Emergency"]
            )
            description = st.text_area("Description of Issue")
            photo = st.file_uploader("Upload Photo (optional)", type=['jpg', 'png'])
            
            submit = st.form_submit_button("Submit Request")
            if submit and description:
                st.success("Maintenance request submitted successfully!")
    
    with col2:
        st.subheader("My Requests")
        requests = fetch_data(f"{ENDPOINTS['housing']}/maintenance-requests")
        if requests and 'results' in requests:
            for request in requests['results']:
                with st.expander(
                    f"{request['type']} - {request['status']} ({request['date']})"
                ):
                    st.write(f"**Description:** {request['description']}")
                    st.write(f"**Priority:** {request['priority']}")
                    if request.get('notes'):
                        st.info(f"**Staff Notes:** {request['notes']}")

# Housing Applications Tab
with tabs[3]:
    st.header("Housing Applications")
    
    # Application Status
    st.subheader("Application Status")
    application = fetch_data(f"{ENDPOINTS['housing']}/application")
    if application:
        st.info(f"Status: {application.get('status', 'No active application')}")
        
        if application.get('status') != 'SUBMITTED':
            # New Application Form
            st.subheader("New Housing Application")
            with st.form("housing_application"):
                semester = st.selectbox(
                    "Semester",
                    ["Fall 2025", "Spring 2026", "Summer 2026"]
                )
                preferences = st.multiselect(
                    "Room Preferences",
                    ["Single Room", "Double Room", "Suite", "Apartment"]
                )
                special_requests = st.text_area("Special Requests/Accommodations")
                roommate_preference = st.text_input("Preferred Roommate (if any)")
                
                col3, col4 = st.columns(2)
                with col3:
                    quiet_study = st.checkbox("Quiet Study Floor")
                with col4:
                    substance_free = st.checkbox("Substance-Free Housing")
                
                submit = st.form_submit_button("Submit Application")
                if submit:
                    st.success("Housing application submitted successfully!")
        else:
            # Display current application details
            st.write("**Application Details:**")
            st.write(f"Semester: {application.get('semester')}")
            st.write(f"Preferences: {', '.join(application.get('preferences', []))}")
            st.write(f"Submission Date: {application.get('submission_date')}")

# Footer
st.markdown("---")
st.markdown("Need help? Contact Housing Services at housing@university.edu") 