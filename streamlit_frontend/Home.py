import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, ROLE_ACCESS, has_module_access
from utils.styles import hide_navigation
import os

# Page config
st.set_page_config(
    page_title="ERP4Uni - Home",
    page_icon="🎓",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Initialize session state for user profile
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None

# Title
st.title("🎓 University ERP System")

# Profile Selection
if not st.session_state.user_role:
    st.header("Select Your Profile")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍🎓 Student", use_container_width=True):
            st.session_state.user_role = 'student'
            st.session_state.user_profile = fetch_data(f"{ENDPOINTS['profile']}/student")
            st.rerun()
    
    with col2:
        if st.button("👨‍🏫 Lecturer", use_container_width=True):
            st.session_state.user_role = 'lecturer'
            st.session_state.user_profile = fetch_data(f"{ENDPOINTS['profile']}/lecturer")
            st.rerun()
    
    with col3:
        if st.button("👨‍💼 Administrator", use_container_width=True):
            st.session_state.user_role = 'admin'
            st.session_state.user_profile = fetch_data(f"{ENDPOINTS['profile']}/admin")
            st.rerun()
    
    st.stop()

# Display current profile
with st.sidebar:
    # Profile Section
    st.markdown("### 👤 Profile")
    if st.session_state.user_profile:
        st.write(f"Welcome, {st.session_state.user_profile.get('full_name', 'User')}")
        st.write(f"Role: {st.session_state.user_profile.get('role', '').title()}")
        if st.button("🚪 Logout"):
            st.session_state.user_role = None
            st.session_state.user_profile = None
            st.rerun()
    
    # Navigation Section
    st.markdown("### 🧭 Navigation")
    
    # Academic Services
    if any(has_module_access(st.session_state.user_role, module) for module in 
           ['Academic Records', 'Faculty Portal', 'Research Management']):
        if has_module_access(st.session_state.user_role, 'Academic Records'):
            if st.button("📚 Academic Records", key="academic_btn", use_container_width=True):
                st.switch_page("pages/4_Academic_Records.py")
        if has_module_access(st.session_state.user_role, 'Faculty Portal'):
            if st.button("👨‍🏫 Faculty Portal", key="faculty_btn", use_container_width=True):
                st.switch_page("pages/5_Faculty_Portal.py")
        if has_module_access(st.session_state.user_role, 'Research Management'):
            if st.button("🔬 Research Management", key="research_btn", use_container_width=True):
                st.switch_page("pages/6_Research_Management.py")
    
    # Administrative Services
    if any(has_module_access(st.session_state.user_role, module) for module in 
           ['Finance & Billing', 'Compliance & Reports', 'Housing Management']):
        if has_module_access(st.session_state.user_role, 'Finance & Billing'):
            if st.button("💰 Finance & Billing", key="finance_sidebar_btn", use_container_width=True):
                st.switch_page("pages/2_Finance_Billing.py")
        if has_module_access(st.session_state.user_role, 'Compliance & Reports'):
            if st.button("📋 Compliance & Reports", key="compliance_btn", use_container_width=True):
                st.switch_page("pages/7_Compliance_Reports.py")
        if has_module_access(st.session_state.user_role, 'Housing Management'):
            if st.button("🏠 Housing Management", key="housing_sidebar_btn", use_container_width=True):
                st.switch_page("pages/3_Housing_Management.py")
    
    # Student Services
    if any(has_module_access(st.session_state.user_role, module) for module in 
           ['Library Services', 'Student Support', 'Campus Life']):
        if has_module_access(st.session_state.user_role, 'Library Services'):
            if st.button("📚 Library Services", key="library_sidebar_btn", use_container_width=True):
                st.switch_page("pages/1_Library_Services.py")
        if has_module_access(st.session_state.user_role, 'Student Support'):
            if st.button("🎯 Student Support", key="support_btn", use_container_width=True):
                st.switch_page("pages/8_Student_Support.py")
        if has_module_access(st.session_state.user_role, 'Campus Life'):
            if st.button("🏫 Campus Life", key="campus_btn", use_container_width=True):
                st.switch_page("pages/9_Campus_Life.py")

# Main content
col1, col2 = st.columns(2)

# Quick Statistics
with col1:
    st.subheader("Quick Statistics")
    
    # Add loading state for stats
    with st.spinner("Loading statistics..."):
        try:
            stats = fetch_data(ENDPOINTS['stats'])
            
            if stats:
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    st.metric("Total Students", 
                             value=stats.get('total_students', 0),
                             delta=stats.get('student_growth', None))
                    st.metric("Total Faculty", 
                             value=stats.get('total_faculty', 0),
                             delta=stats.get('faculty_growth', None))
                    st.metric("Active Courses", 
                             value=stats.get('active_courses', 0))
                
                with metrics_col2:
                    st.metric("Departments", 
                             value=stats.get('total_departments', 0))
                    housing = stats.get('housing_occupancy', {})
                    occupancy = 0
                    if housing.get('total_capacity') and housing.get('total_occupied'):
                        occupancy = round((housing['total_occupied'] / housing['total_capacity']) * 100)
                    st.metric("Housing Occupancy", 
                             value=f"{occupancy}%",
                             delta=f"{stats.get('occupancy_change', 0)}%" if stats.get('occupancy_change') else None)
                    st.metric("Research Projects", 
                             value=stats.get('research_projects', 0),
                             delta=stats.get('project_growth', None))
            else:
                st.error("Unable to load statistics. Please try again later.")
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")

# System Status
with col2:
    st.subheader("System Status")
    
    # Academic Period with loading state
    st.write("**Current Academic Period**")
    with st.spinner("Loading academic year information..."):
        try:
            academic_years = fetch_data(ENDPOINTS['academic_years'])
            if academic_years and 'results' in academic_years:
                active_year = next((year for year in academic_years['results'] if year.get('is_active')), None)
                if active_year:
                    st.info(f"Academic Year: {active_year['year']}")
                else:
                    st.warning("No active academic year set")
            else:
                st.error("Unable to load academic year information")
        except Exception as e:
            st.error(f"Error loading academic year: {str(e)}")
    
    # Upcoming Deadlines
    st.write("**Upcoming Deadlines**")
    with st.spinner("Loading deadlines..."):
        try:
            deadlines = [
                {"event": "Course Registration", "date": "March 15, 2025", "days_left": 30},
                {"event": "Housing Applications", "date": "April 1, 2025", "days_left": 45},
                {"event": "Research Grant Submissions", "date": "March 30, 2025", "days_left": 40},
                {"event": "Library Book Returns", "date": "March 10, 2025", "days_left": 25},
                {"event": "Financial Aid Applications", "date": "March 20, 2025", "days_left": 35}
            ]
            
            # Filter deadlines based on user role
            filtered_deadlines = []
            for deadline in deadlines:
                # Map deadline events to modules
                module_mapping = {
                    "Course Registration": "Academic Records",
                    "Housing Applications": "Housing Management",
                    "Research Grant Submissions": "Research Management",
                    "Library Book Returns": "Library Services",
                    "Financial Aid Applications": "Finance & Billing"
                }
                
                if module_mapping.get(deadline["event"]) and \
                   has_module_access(st.session_state.user_role, module_mapping[deadline["event"]]):
                    filtered_deadlines.append(deadline)
            
            for deadline in filtered_deadlines:
                days_text = f"({deadline['days_left']} days left)"
                st.write(f"• {deadline['event']}: {deadline['date']} {days_text}")
        except Exception as e:
            st.error(f"Error loading deadlines: {str(e)}")

# Recent Activities with loading state
st.subheader("Recent Activities")
with st.spinner("Loading recent activities..."):
    try:
        activities_response = fetch_data(ENDPOINTS['recent_activities'])
        
        if activities_response and 'activities' in activities_response:
            activities = activities_response['activities']
            if activities:
                # Filter activities based on user role
                filtered_activities = []
                for activity in activities:
                    # Map activity categories to modules
                    module_mapping = {
                        "Academic": "Academic Records",
                        "Library": "Library Services",
                        "Housing": "Housing Management",
                        "Finance": "Finance & Billing",
                        "Research": "Research Management"
                    }
                    
                    if module_mapping.get(activity.get("category")) and \
                       has_module_access(st.session_state.user_role, module_mapping[activity["category"]]):
                        filtered_activities.append(activity)
                
                for activity in filtered_activities:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            description = activity.get('description', 'No description available')
                            category = activity.get('category', '')
                            if category:
                                st.write(f"• [{category}] {description}")
                            else:
                                st.write(f"• {description}")
                        with col2:
                            date = activity.get('date', '')
                            if date:
                                try:
                                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                                    st.write(date_obj.strftime('%b %d, %Y'))
                                except:
                                    st.write(date)
            else:
                st.info("No recent activities to display")
        else:
            st.warning("Unable to load recent activities")
    except Exception as e:
        st.error(f"Error loading activities: {str(e)}")

# Quick Access Cards
st.subheader("Quick Access")
col1, col2, col3 = st.columns(3)

# Only show Quick Access cards for modules the user has access to
with col1:
    if has_module_access(st.session_state.user_role, 'Library Services'):
        with st.container():
            st.info("**📚 Library Services**\nSearch books, manage borrowings, and reserve study rooms.")
            if st.button("Access Library Services", key="library_btn", use_container_width=True):
                st.switch_page("pages/1_Library_Services.py")

with col2:
    if has_module_access(st.session_state.user_role, 'Finance & Billing'):
        with st.container():
            st.info("**💰 Finance & Billing**\nView fees, make payments, and check financial aid status.")
            if st.button("Access Finance & Billing", key="finance_btn", use_container_width=True):
                st.switch_page("pages/2_Finance_Billing.py")

with col3:
    if has_module_access(st.session_state.user_role, 'Housing Management'):
        with st.container():
            st.info("**🏠 Housing Management**\nApply for housing, submit maintenance requests, and check room status.")
            if st.button("Access Housing Management", key="housing_btn", use_container_width=True):
                st.switch_page("pages/3_Housing_Management.py")

# Footer
st.markdown("---")
st.markdown(f"© {datetime.now().year} ERP4Uni. All rights reserved.")
st.markdown("Need help? Contact support@university.edu")
