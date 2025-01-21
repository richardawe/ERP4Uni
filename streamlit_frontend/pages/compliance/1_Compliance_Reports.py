import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Compliance & Reports - ERP4Uni",
    page_icon="📋",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("📋 Compliance & Reports")

# Create tabs for different sections
tabs = st.tabs(["Regulatory Reports", "Compliance Status", "Active Audits", "Policy Documentation"])

# Regulatory Reports Tab
with tabs[0]:
    st.header("Regulatory Reports")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generate Report")
        with st.form("report_generation"):
            report_type = st.selectbox(
                "Report Category",
                ["Financial Compliance", "Academic Standards", "Research Ethics", 
                 "Student Services", "Safety & Security"]
            )
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            include_sections = st.multiselect(
                "Include Sections",
                ["Summary Statistics", "Detailed Analysis", "Recommendations", 
                 "Supporting Documents", "Action Items"]
            )
            output_format = st.radio(
                "Output Format",
                ["PDF", "Excel", "Word"]
            )
            
            submit = st.form_submit_button("Generate Report")
            if submit:
                st.success("Report generation initiated. You will be notified when it's ready.")
    
    with col2:
        st.subheader("Recent Reports")
        reports = fetch_data(f"{ENDPOINTS['compliance-reports']}")
        if reports and 'results' in reports:
            df = pd.DataFrame(reports['results'])
            if not df.empty:
                st.dataframe(
                    df[['name', 'generated_date', 'generated_by', 'status']],
                    hide_index=True
                )

# Compliance Status Tab
with tabs[1]:
    st.header("Compliance Status")
    
    # Overall compliance metrics
    col1, col2, col3 = st.columns(3)
    metrics = fetch_data(f"{ENDPOINTS['compliance-reports']}/metrics")
    if metrics:
        with col1:
            st.metric("Overall Compliance Score", f"{metrics.get('compliance_score', 0)}%")
        with col2:
            st.metric("Open Issues", metrics.get('open_issues', 0))
        with col3:
            st.metric("Next Audit Due", metrics.get('next_audit_date', 'N/A'))
    
    # Compliance checklist
    st.subheader("Compliance Checklist")
    
    # Financial Compliance
    with st.expander("Financial Compliance"):
        st.checkbox("Annual Financial Audit Complete", value=True)
        st.checkbox("Tax Compliance Documentation Updated")
        st.checkbox("Financial Controls Review Complete", value=True)
    
    # Academic Compliance
    with st.expander("Academic Compliance"):
        st.checkbox("Accreditation Requirements Met", value=True)
        st.checkbox("Faculty Qualifications Updated")
        st.checkbox("Curriculum Review Complete")
    
    # Research Compliance
    with st.expander("Research Compliance"):
        st.checkbox("IRB Protocols Updated", value=True)
        st.checkbox("Research Ethics Training Complete")
        st.checkbox("Grant Compliance Review")

# Active Audits Tab
with tabs[2]:
    st.header("Active Audits")
    
    # Fetch active audits
    audits = fetch_data(f"{ENDPOINTS['audits']}?status=IN_PROGRESS")
    if audits and 'results' in audits:
        for audit in audits['results']:
            with st.expander(f"{audit['title']} - {audit['status']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Department:** {audit['department']}")
                    st.write(f"**Auditor:** {audit['auditor']}")
                    st.write(f"**Timeline:** {audit['start_date']} to {audit['end_date']}")
                    st.write(f"**Scope:** {audit['scope']}")
                with col2:
                    st.metric("Progress", f"{audit['progress']}%")
                    st.metric("Findings", audit['findings_count'])
                
                # Findings
                if audit.get('findings'):
                    st.subheader("Audit Findings")
                    for finding in audit['findings']:
                        st.warning(f"**{finding['severity']}:** {finding['description']}")

# Policy Documentation Tab
with tabs[3]:
    st.header("Policy Documentation")
    
    # Policy search
    st.subheader("Search Policies")
    search = st.text_input("Search policies...")
    
    # Policy categories
    categories = ["Academic", "Administrative", "Financial", "Research", "Student Services"]
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Display policies
    for category in categories:
        if selected_category in ["All", category]:
            with st.expander(f"{category} Policies"):
                policies = fetch_data(f"{ENDPOINTS['policies']}?category={category}")
                if policies and 'results' in policies:
                    for policy in policies['results']:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{policy['title']}**")
                            st.write(f"Last Updated: {policy['last_updated']}")
                        with col2:
                            st.download_button(
                                "Download",
                                policy['document'],
                                file_name=f"{policy['title']}.pdf"
                            )

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Compliance Office at compliance@university.edu") 