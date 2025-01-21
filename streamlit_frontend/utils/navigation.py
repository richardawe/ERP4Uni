import streamlit as st
from utils.api import has_module_access

def show_navigation():
    """Show the profile and navigation sidebar"""
    with st.sidebar:
        # Profile Section
        st.markdown("### 👤 Profile")
        if st.session_state.user_profile:
            st.write(f"Welcome, {st.session_state.user_profile.get('full_name', 'User')}")
            st.write(f"Role: {st.session_state.user_profile.get('role', '').title()}")
            if st.button("🚪 Logout", key="nav_logout_btn"):
                st.session_state.user_role = None
                st.session_state.user_profile = None
                st.switch_page("Home.py")
        
        # Navigation Section
        st.markdown("### 🧭 Navigation")
        
        # Academic Services
        if any(has_module_access(st.session_state.user_role, module) for module in 
               ['Academic Records', 'Faculty Portal', 'Research Management']):
            st.markdown("#### Academic Services")
            if has_module_access(st.session_state.user_role, 'Academic Records'):
                if st.button("📚 Academic Records", key="nav_academic_btn", use_container_width=True):
                    st.switch_page("pages/4_Academic_Records.py")
            if has_module_access(st.session_state.user_role, 'Faculty Portal'):
                if st.button("👨‍🏫 Faculty Portal", key="nav_faculty_btn", use_container_width=True):
                    st.switch_page("pages/5_Faculty_Portal.py")
            if has_module_access(st.session_state.user_role, 'Research Management'):
                if st.button("🔬 Research Management", key="nav_research_btn", use_container_width=True):
                    st.switch_page("pages/6_Research_Management.py")
        
        # Administrative Services
        if any(has_module_access(st.session_state.user_role, module) for module in 
               ['Finance & Billing', 'Compliance & Reports', 'Housing Management']):
            st.markdown("#### Administrative Services")
            if has_module_access(st.session_state.user_role, 'Finance & Billing'):
                if st.button("💰 Finance & Billing", key="nav_finance_btn", use_container_width=True):
                    st.switch_page("pages/2_Finance_Billing.py")
            if has_module_access(st.session_state.user_role, 'Compliance & Reports'):
                if st.button("📋 Compliance & Reports", key="nav_compliance_btn", use_container_width=True):
                    st.switch_page("pages/7_Compliance_Reports.py")
            if has_module_access(st.session_state.user_role, 'Housing Management'):
                if st.button("🏠 Housing Management", key="nav_housing_btn", use_container_width=True):
                    st.switch_page("pages/3_Housing_Management.py")
        
        # Student Services
        if any(has_module_access(st.session_state.user_role, module) for module in 
               ['Library Services', 'Student Support', 'Campus Life']):
            st.markdown("#### Student Services")
            if has_module_access(st.session_state.user_role, 'Library Services'):
                if st.button("📚 Library Services", key="nav_library_btn", use_container_width=True):
                    st.switch_page("pages/1_Library_Services.py")
            if has_module_access(st.session_state.user_role, 'Student Support'):
                if st.button("🎯 Student Support", key="nav_support_btn", use_container_width=True):
                    st.switch_page("pages/8_Student_Support.py")
            if has_module_access(st.session_state.user_role, 'Campus Life'):
                if st.button("🏫 Campus Life", key="nav_campus_btn", use_container_width=True):
                    st.switch_page("pages/9_Campus_Life.py")

def check_access():
    """Check if user is logged in and has access to the page"""
    # Initialize session state for user profile if not exists
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    # Check if user is logged in
    if not st.session_state.user_role:
        st.warning("Please log in to access this page.")
        if st.button("Go to Login", key="nav_login_btn"):
            st.switch_page("Home.py")
        st.stop() 