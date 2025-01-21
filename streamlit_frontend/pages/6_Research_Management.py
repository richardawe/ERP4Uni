from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Research Management - ERP4Uni",
    page_icon="🔬",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("🔬 Research Management")

# Create tabs for different sections
tabs = st.tabs(["Research Grants", "Active Projects", "Publications", "Research Analytics"])

# Research Grants Tab
with tabs[0]:
    st.subheader("Available Grants")
    grants_df = pd.DataFrame({
        "Grant Name": ["Innovation Fund", "Tech Research Grant", "Science Development"],
        "Amount": ["$100,000", "$75,000", "$50,000"],
        "Deadline": ["2024-03-15", "2024-04-01", "2024-03-30"],
        "Status": ["Open", "Open", "Reviewing"]
    })
    st.dataframe(grants_df)
    
    st.subheader("Grant Application")
    col1, col2 = st.columns(2)
    with col1:
        grant_name = st.selectbox("Select Grant", ["Innovation Fund", "Tech Research Grant"])
        project_title = st.text_input("Project Title")
        duration = st.selectbox("Project Duration", ["6 months", "1 year", "2 years"])
    with col2:
        budget = st.number_input("Requested Budget ($)", min_value=1000, max_value=100000, value=50000)
        team_size = st.number_input("Team Size", min_value=1, max_value=10, value=3)
    
    abstract = st.text_area("Project Abstract")
    uploaded_files = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
    if st.button("Submit Application"):
        st.success("Grant application submitted successfully!")

# Active Projects Tab
with tabs[1]:
    st.subheader("Project Overview")
    projects_df = pd.DataFrame({
        "Project": ["AI Research", "Blockchain Study", "Green Energy"],
        "PI": ["Dr. Smith", "Dr. Johnson", "Dr. Williams"],
        "Timeline": ["Jan 2024 - Jun 2024", "Mar 2024 - Feb 2025", "Jan 2024 - Dec 2024"],
        "Budget Spent": ["$25,000", "$15,000", "$30,000"],
        "Status": ["On Track", "Planning", "Delayed"]
    })
    st.dataframe(projects_df)
    
    st.subheader("Project Details")
    col1, col2 = st.columns(2)
    with col1:
        selected_project = st.selectbox("Select Project", ["AI Research", "Blockchain Study", "Green Energy"])
        st.metric("Budget Remaining", "$75,000")
        st.metric("Time Remaining", "120 days")
    with col2:
        st.metric("Team Members", "5")
        st.metric("Milestones Completed", "3/8")
    
    st.subheader("Project Milestones")
    milestones_df = pd.DataFrame({
        "Milestone": ["Literature Review", "Data Collection", "Initial Analysis"],
        "Due Date": ["2024-02-15", "2024-03-30", "2024-04-30"],
        "Status": ["Completed", "In Progress", "Pending"],
        "Notes": ["Documentation complete", "50% data collected", "Team assigned"]
    })
    st.dataframe(milestones_df)

# Publications Tab
with tabs[2]:
    st.subheader("Research Publications")
    publications_df = pd.DataFrame({
        "Title": ["AI in Education", "Blockchain Applications", "Renewable Energy"],
        "Authors": ["Smith et al.", "Johnson et al.", "Williams et al."],
        "Journal": ["Tech Journal", "Blockchain Review", "Energy Science"],
        "Impact Factor": [3.5, 2.8, 4.2],
        "Citations": [25, 18, 30]
    })
    st.dataframe(publications_df)
    
    st.subheader("Add Publication")
    col1, col2 = st.columns(2)
    with col1:
        pub_title = st.text_input("Publication Title")
        authors = st.text_input("Authors")
        journal = st.text_input("Journal/Conference")
    with col2:
        pub_date = st.date_input("Publication Date")
        doi = st.text_input("DOI")
        impact_factor = st.number_input("Impact Factor", min_value=0.0, max_value=50.0, value=1.0)
    
    if st.button("Add Publication"):
        st.success("Publication added successfully!")

# Research Analytics Tab
with tabs[3]:
    st.subheader("Research Metrics")
    
    # Funding Distribution
    st.write("**Funding Distribution by Department**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Active Grants", "$450,000")
        st.metric("Pending Applications", "$250,000")
    with col2:
        st.metric("Success Rate", "75%")
        st.metric("Average Grant Size", "$85,000")
    
    # Publication Metrics
    st.write("**Publication Analytics**")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total Publications", "45")
        st.metric("Average Impact Factor", "3.2")
    with col4:
        st.metric("Total Citations", "850")
        st.metric("H-index", "15")

# Footer
st.markdown("---")
st.markdown("Need help? Contact research.office@university.edu or visit the Research Office") 