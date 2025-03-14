from config import ENDPOINTS
from utils.api import fetch_data, post_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Compliance & Reports - ERP4Uni",
    page_icon="📋",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("📋 Compliance & Reports")

# Create tabs for different sections
tabs = st.tabs(["Regulatory Reports", "Compliance Status", "Active Audits", "Policy Documentation"])

# Regulatory Reports Tab
with tabs[0]:
    st.subheader("Generate Report")
    
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Category", 
            ["Financial Compliance", "Academic Standards", "Research Ethics", 
             "Student Services", "Safety & Security"])
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
        output_format = st.selectbox("Output Format", ["PDF", "Excel", "Word"])
    
    sections = st.multiselect("Include Sections",
        ["Executive Summary", "Detailed Metrics", "Compliance Status",
         "Risk Assessment", "Recommendations", "Supporting Documents"])
    
    if st.button("Generate Report"):
        st.success("Report generated successfully! Check your email for the download link.")
    
    st.subheader("Recent Reports")
    reports_df = pd.DataFrame({
        "Report Name": ["Q4 Financial Compliance", "Annual Academic Review", "Research Ethics Audit"],
        "Generated Date": ["2024-01-15", "2023-12-20", "2023-12-01"],
        "Generated By": ["John Smith", "Sarah Johnson", "Mike Wilson"],
        "Status": ["Complete", "Under Review", "Approved"]
    })
    st.dataframe(reports_df)

# Compliance Status Tab
with tabs[1]:
    st.subheader("Compliance Overview")
    
    # Compliance Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Compliance Score", "92%")
        st.metric("Open Issues", "5")
    with col2:
        st.metric("Critical Issues", "0")
        st.metric("Warnings", "3")
    with col3:
        st.metric("Next Audit Due", "30 days")
        st.metric("Last Updated", "2024-01-20")
    
    # Compliance Checklist
    st.subheader("Compliance Checklist")
    
    # Financial Compliance
    with st.expander("Financial Compliance"):
        st.checkbox("Annual Budget Review", value=True)
        st.checkbox("Financial Audits", value=True)
        st.checkbox("Grant Management", value=True)
        st.checkbox("Tax Compliance", value=False)
    
    # Academic Compliance
    with st.expander("Academic Compliance"):
        st.checkbox("Accreditation Standards", value=True)
        st.checkbox("Faculty Qualifications", value=True)
        st.checkbox("Curriculum Review", value=True)
        st.checkbox("Student Assessment", value=True)
    
    # Research Compliance
    with st.expander("Research Compliance"):
        st.checkbox("Ethics Review", value=True)
        st.checkbox("Research Safety", value=True)
        st.checkbox("Data Management", value=False)
        st.checkbox("Grant Reporting", value=True)

# Active Audits Tab
with tabs[2]:
    st.subheader("Ongoing Audits")
    audits_df = pd.DataFrame({
        "Department": ["Finance", "Academic Affairs", "Research"],
        "Auditor": ["External Firm", "Internal Team", "Accreditation Body"],
        "Start Date": ["2024-01-10", "2024-01-15", "2024-02-01"],
        "End Date": ["2024-02-10", "2024-02-15", "2024-03-01"],
        "Status": ["In Progress", "Planning", "Scheduled"]
    })
    st.dataframe(audits_df)
    
    st.subheader("Audit Findings")
    findings_df = pd.DataFrame({
        "Finding": ["Budget Variance", "Documentation Gap", "Process Improvement"],
        "Severity": ["Medium", "Low", "Low"],
        "Department": ["Finance", "Academic", "Research"],
        "Due Date": ["2024-03-01", "2024-02-15", "2024-02-28"],
        "Status": ["Open", "In Progress", "Open"]
    })
    st.dataframe(findings_df)
    
    st.subheader("Schedule Audit")
    col1, col2 = st.columns(2)
    with col1:
        audit_dept = st.selectbox("Department", ["Finance", "Academic Affairs", "Research", "Student Services"])
        audit_type = st.selectbox("Audit Type", ["Internal", "External", "Compliance"])
    with col2:
        audit_start = st.date_input("Start Date", key="audit_start")
        audit_duration = st.number_input("Duration (days)", min_value=1, max_value=90, value=30)
    
    if st.button("Schedule Audit"):
        st.success("Audit scheduled successfully!")

# Policy Documentation Tab
with tabs[3]:
    st.subheader("Policy Search")
    search = st.text_input("Search Policies")
    
    # Financial Policies
    st.write("**Financial Policies**")
    fin_policies = pd.DataFrame({
        "Policy": ["Budget Management", "Expense Reporting", "Grant Administration"],
        "Last Updated": ["2024-01-01", "2023-12-15", "2023-12-01"],
        "Status": ["Active", "Active", "Under Review"]
    })
    st.dataframe(fin_policies)
    
    # Academic Policies
    st.write("**Academic Policies**")
    acad_policies = pd.DataFrame({
        "Policy": ["Grading Standards", "Academic Integrity", "Course Development"],
        "Last Updated": ["2024-01-10", "2023-12-20", "2023-12-05"],
        "Status": ["Active", "Active", "Active"]
    })
    st.dataframe(acad_policies)
    
    # Research Policies
    st.write("**Research Policies**")
    research_policies = pd.DataFrame({
        "Policy": ["Research Ethics", "Data Management", "Grant Proposals"],
        "Last Updated": ["2024-01-05", "2023-12-10", "2023-12-01"],
        "Status": ["Active", "Active", "Active"]
    })
    st.dataframe(research_policies)

# Footer
st.markdown("---")
st.markdown("Need help? Contact compliance@university.edu or visit the Compliance Office") 