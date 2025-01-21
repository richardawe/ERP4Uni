import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Research Management - ERP4Uni",
    page_icon="🔬",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("🔬 Research Management")

# Create tabs for different sections
tabs = st.tabs(["Research Grants", "Active Projects", "Publications", "Research Analytics"])

# Research Grants Tab
with tabs[0]:
    st.header("Research Grants")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Available Grants")
        # Fetch available grants from API
        grants = fetch_data(f"{ENDPOINTS['research-grants']}?status=OPEN")
        if grants and 'results' in grants:
            df = pd.DataFrame(grants['results'])
            if not df.empty:
                st.dataframe(
                    df[['title', 'funding_amount', 'deadline', 'status']],
                    hide_index=True
                )
            else:
                st.info("No open grants available at this time.")
    
    with col2:
        st.subheader("Apply for Grant")
        with st.form("grant_application"):
            grant_title = st.text_input("Project Title")
            amount = st.number_input("Requested Amount ($)", min_value=1000, step=1000)
            duration = st.number_input("Project Duration (months)", min_value=1, max_value=60)
            category = st.selectbox(
                "Research Category",
                ["Technology", "Science", "Medicine", "Humanities", "Social Sciences"]
            )
            abstract = st.text_area("Project Abstract")
            
            submit = st.form_submit_button("Submit Application")
            if submit and grant_title and abstract:
                st.success("Grant application submitted successfully!")

# Active Projects Tab
with tabs[1]:
    st.header("Research Projects")
    
    # Fetch active projects from API
    projects = fetch_data(f"{ENDPOINTS['research-projects']}?status=IN_PROGRESS")
    if projects and 'results' in projects:
        for project in projects['results']:
            with st.expander(f"{project['title']} - {project['status']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**PI:** {project['principal_investigator']}")
                    st.write(f"**Timeline:** {project['start_date']} to {project['end_date']}")
                    st.write(f"**Budget:** ${project['budget']:,.2f}")
                    st.write(f"**Description:** {project['description']}")
                with col2:
                    st.metric("Progress", f"{project['progress']}%")
                    st.metric("Budget Used", f"{project['budget_used']}%")
                
                # Milestones
                st.subheader("Milestones")
                milestones_df = pd.DataFrame(project['milestones'])
                if not milestones_df.empty:
                    st.dataframe(
                        milestones_df[['description', 'due_date', 'status']],
                        hide_index=True
                    )

# Publications Tab
with tabs[2]:
    st.header("Research Publications")
    
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
            abstract = st.text_area("Abstract")
            
            submit = st.form_submit_button("Add Publication")
            if submit and title and authors and venue:
                st.success("Publication added successfully!")
    
    with col2:
        st.subheader("Publication Metrics")
        metrics = fetch_data(f"{ENDPOINTS['publications']}/metrics")
        if metrics:
            st.metric("Total Publications", metrics.get('total', 0))
            st.metric("Citations", metrics.get('citations', 0))
            st.metric("h-index", metrics.get('h_index', 0))

# Research Analytics Tab
with tabs[3]:
    st.header("Research Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funding Distribution")
        funding_data = {
            "Technology": 30,
            "Science": 25,
            "Medicine": 20,
            "Humanities": 15,
            "Social Sciences": 10
        }
        st.bar_chart(funding_data)
    
    with col2:
        st.subheader("Publication Trends")
        years = list(range(datetime.now().year - 4, datetime.now().year + 1))
        pub_trends = {str(year): year % 10 + 5 for year in years}  # Sample data
        st.line_chart(pub_trends)
    
    # Research Collaboration Network
    st.subheader("Research Collaboration Network")
    collaborations = fetch_data(f"{ENDPOINTS['research-projects']}/collaborations")
    if collaborations and 'results' in collaborations:
        st.dataframe(
            pd.DataFrame(collaborations['results']),
            hide_index=True
        )

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Research Office at research.office@university.edu") 