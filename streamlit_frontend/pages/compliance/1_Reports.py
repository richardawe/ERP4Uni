import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data

def render_regulatory_reports():
    st.subheader("Regulatory Reports")
    
    # Report categories
    report_type = st.selectbox(
        "Report Category",
        ["Enrollment Statistics", "Financial Reports", "Academic Performance", "Research Compliance"]
    )
    
    # Report generation form
    with st.form("generate_report"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
            
        include_sections = st.multiselect(
            "Include Sections",
            ["Summary Statistics", "Detailed Analysis", "Charts and Graphs", "Raw Data"]
        )
        
        file_format = st.radio("Output Format", ["PDF", "Excel", "CSV"])
        
        submitted = st.form_submit_button("Generate Report")
        if submitted:
            st.success("Report generated successfully!")
            st.download_button(
                "Download Report",
                "dummy_data",
                f"report_{datetime.now().strftime('%Y%m%d')}.{file_format.lower()}"
            )
    
    # Recent reports
    st.subheader("Recent Reports")
    reports = pd.DataFrame({
        'Report Name': ['Enrollment Report Q4', 'Financial Audit 2024', 'Research Ethics Review'],
        'Generated On': ['2025-01-15', '2025-01-10', '2025-01-05'],
        'Generated By': ['Admin User', 'Finance Dept', 'Research Office'],
        'Status': ['Complete', 'Under Review', 'Approved']
    })
    st.dataframe(reports)

def render_compliance():
    st.subheader("Compliance & Audits")
    
    # Compliance status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance Score", "92%")
    with col2:
        st.metric("Open Issues", "3")
    with col3:
        st.metric("Next Audit", "Mar 15, 2025")
    
    # Active audits
    st.subheader("Active Audits")
    audits = pd.DataFrame({
        'Audit Type': ['Financial', 'Academic', 'Research Ethics'],
        'Start Date': ['2025-01-01', '2025-02-01', '2025-03-01'],
        'Due Date': ['2025-02-28', '2025-03-31', '2025-04-30'],
        'Status': ['In Progress', 'Planned', 'Planned'],
        'Assigned To': ['Finance Team', 'Academic Affairs', 'Ethics Committee']
    })
    st.dataframe(audits)
    
    # Compliance checklist
    st.subheader("Compliance Checklist")
    with st.expander("Financial Compliance"):
        st.checkbox("Annual Budget Review", value=True)
        st.checkbox("Grant Expenditure Audit", value=True)
        st.checkbox("Financial Controls Assessment", value=False)
    
    with st.expander("Academic Compliance"):
        st.checkbox("Course Evaluations Complete", value=True)
        st.checkbox("Faculty Qualifications Review", value=True)
        st.checkbox("Student Progress Monitoring", value=True)
    
    with st.expander("Research Compliance"):
        st.checkbox("Ethics Approvals", value=True)
        st.checkbox("Research Data Management", value=False)
        st.checkbox("Grant Compliance Review", value=True)

def render_documentation():
    st.subheader("Policy Documentation")
    
    # Policy search
    search = st.text_input("Search Policies")
    
    # Policy categories
    policies = {
        "Academic Policies": [
            "Academic Integrity Policy",
            "Course Registration Guidelines",
            "Grading Policy"
        ],
        "Administrative Policies": [
            "HR Procedures",
            "Financial Guidelines",
            "IT Usage Policy"
        ],
        "Research Policies": [
            "Research Ethics Guidelines",
            "Grant Management Procedures",
            "Data Protection Policy"
        ]
    }
    
    for category, policy_list in policies.items():
        with st.expander(category):
            for policy in policy_list:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(policy)
                with col2:
                    st.download_button(
                        "Download",
                        "dummy_data",
                        f"{policy.lower().replace(' ', '_')}.pdf"
                    )

# Main page content
st.title("📋 Compliance & Reports")

# Create tabs for different functions
tabs = st.tabs(["Regulatory Reports", "Compliance & Audits", "Documentation"])

with tabs[0]:
    render_regulatory_reports()

with tabs[1]:
    render_compliance()

with tabs[2]:
    render_documentation() 