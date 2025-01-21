from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data, get_mock_profile
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Housing Management - ERP4Uni",
    page_icon="🏠",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("🏠 Housing Management")

# Create tabs for different sections
tabs = st.tabs(["Room Status", "Housing Application", "Maintenance Requests", "Room Assignment"])

# Room Status Tab
with tabs[0]:
    st.subheader("Current Room Status")
    
    with st.spinner("Loading room information..."):
        # Initialize user_profile if not present
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = get_mock_profile('student')
        
        housing_info = fetch_data(ENDPOINTS['housing'])
        if housing_info and isinstance(housing_info.get('results', None), dict):
            data = housing_info['results']
            
            # Display room information
            col1, col2 = st.columns(2)
            with col1:
                st.info("Room Details")
                st.write(f"Building: {data.get('building', 'Not assigned')}")
                st.write(f"Room Number: {data.get('room_number', 'Not assigned')}")
                st.write(f"Room Type: {data.get('room_type', 'Not assigned')}")
            with col2:
                st.info("Contract Details")
                st.write(f"Start Date: {data.get('contract_start', 'Not set')}")
                st.write(f"End Date: {data.get('contract_end', 'Not set')}")
                st.write(f"Status: {data.get('status', 'Unknown')}")
        else:
            st.info("No current room assignment found.")

# Housing Application Tab
with tabs[1]:
    st.subheader("Apply for Housing")
    
    col1, col2 = st.columns(2)
    with col1:
        preferred_building = st.selectbox(
            "Preferred Building",
            ["North Hall", "South Hall", "East Hall", "West Hall"]
        )
        room_type = st.selectbox(
            "Room Type",
            ["Single", "Double", "Suite", "Apartment"]
        )
    with col2:
        term = st.selectbox(
            "Term",
            ["Fall 2024", "Spring 2025", "Summer 2025"]
        )
        meal_plan = st.selectbox(
            "Meal Plan",
            ["None", "Basic", "Standard", "Premium"]
        )
    
    special_requests = st.text_area("Special Requests/Accommodations")
    
    if st.button("Submit Application", key="submit_housing_app"):
        with st.spinner("Submitting application..."):
            application_data = {
                'user_id': st.session_state.user_profile['id'],
                'preferred_building': preferred_building,
                'room_type': room_type,
                'term': term,
                'meal_plan': meal_plan,
                'special_requests': special_requests,
                'date_applied': datetime.now().isoformat()
            }
            response = post_data(ENDPOINTS['housing_applications'], application_data)
            if response and response.get('status') == 'success':
                st.success("Housing application submitted successfully!")
            else:
                st.error("Failed to submit application. Please try again.")

# Maintenance Requests Tab
with tabs[2]:
    st.subheader("Maintenance Requests")
    
    # Show existing requests
    with st.spinner("Loading maintenance requests..."):
        requests = fetch_data(ENDPOINTS['maintenance_requests'])
        if requests and 'results' in requests:
            st.dataframe(pd.DataFrame(requests['results']))
    
    # New request form
    st.subheader("Submit New Request")
    request_type = st.selectbox(
        "Request Type",
        ["Plumbing", "Electrical", "Furniture", "HVAC", "Cleaning", "Other"]
    )
    priority = st.select_slider(
        "Priority Level",
        options=["Low", "Medium", "High", "Emergency"]
    )
    description = st.text_area("Description of Issue")
    
    if st.button("Submit Request", key="submit_maintenance"):
        if not description:
            st.error("Please provide a description of the issue.")
        else:
            with st.spinner("Submitting request..."):
                request_data = {
                    'user_id': st.session_state.user_profile['id'],
                    'request_type': request_type,
                    'priority': priority,
                    'description': description,
                    'date_submitted': datetime.now().isoformat()
                }
                response = post_data(ENDPOINTS['maintenance_requests'], request_data)
                if response and response.get('status') == 'success':
                    st.success("Maintenance request submitted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to submit request. Please try again.")

# Room Assignment Tab (Admin Only)
with tabs[3]:
    user_role = st.session_state.user_profile.get('role', 'student')
    if user_role == 'admin':
        st.subheader("Room Assignments")
        
        # Load pending applications
        with st.spinner("Loading pending applications..."):
            applications = fetch_data(ENDPOINTS['housing_applications'])
            if applications and 'results' in applications:
                st.dataframe(pd.DataFrame(applications['results']))
        
        # Assignment form
        st.subheader("Assign Room")
        student_id = st.text_input("Student ID")
        col1, col2 = st.columns(2)
        with col1:
            building = st.selectbox(
                "Building",
                ["North Hall", "South Hall", "East Hall", "West Hall"],
                key="assign_building"
            )
            room_number = st.text_input("Room Number")
        with col2:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
        
        if st.button("Assign Room", key="assign_room"):
            if not all([student_id, building, room_number, start_date, end_date]):
                st.error("Please fill in all required fields.")
            else:
                with st.spinner("Processing assignment..."):
                    assignment_data = {
                        'student_id': student_id,
                        'building': building,
                        'room_number': room_number,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                    response = post_data(ENDPOINTS['room_assignments'], assignment_data)
                    if response and response.get('status') == 'success':
                        st.success("Room assigned successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to assign room. Please try again.")
    else:
        st.info("Room assignment access is restricted to administrative staff.")

# Footer
st.markdown("---")
st.markdown("Need help? Contact housing@erp4uni.edu or visit the Housing Office") 