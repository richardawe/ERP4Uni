import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Finance & Billing - ERP4Uni",
    page_icon="💰",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("💰 Finance & Billing")

# Create tabs for different sections
tabs = st.tabs(["Financial Summary", "Payments", "Scholarships", "Financial Aid"])

# Financial Summary Tab
with tabs[0]:
    st.header("Financial Summary")
    
    # Financial Overview
    col1, col2, col3 = st.columns(3)
    
    # Fetch financial data from API
    financial_data = fetch_data(f"{ENDPOINTS['finance']}/summary")
    if financial_data:
        with col1:
            st.metric("Total Fees", f"${financial_data.get('total_fees', 0):,.2f}")
            st.metric("Paid Amount", f"${financial_data.get('paid_amount', 0):,.2f}")
        with col2:
            st.metric("Balance Due", f"${financial_data.get('balance_due', 0):,.2f}")
            st.metric("Next Payment", f"${financial_data.get('next_payment', 0):,.2f}")
        with col3:
            st.metric("Due Date", financial_data.get('due_date', 'N/A'))
            st.metric("Payment Status", financial_data.get('payment_status', 'N/A'))
    
    # Transaction History
    st.subheader("Recent Transactions")
    transactions = fetch_data(f"{ENDPOINTS['finance']}/transactions")
    if transactions and 'results' in transactions:
        df = pd.DataFrame(transactions['results'])
        if not df.empty:
            st.dataframe(
                df[['date', 'description', 'amount', 'type', 'status']],
                hide_index=True
            )

# Payments Tab
with tabs[1]:
    st.header("Make a Payment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("payment_form"):
            payment_type = st.selectbox(
                "Payment Type",
                ["Tuition", "Housing", "Meal Plan", "Books", "Other Fees"]
            )
            amount = st.number_input("Amount ($)", min_value=1.0, step=0.01)
            payment_method = st.selectbox(
                "Payment Method",
                ["Credit Card", "Bank Transfer", "Check"]
            )
            
            if payment_method == "Credit Card":
                st.text_input("Card Number")
                col3, col4 = st.columns(2)
                with col3:
                    st.text_input("Expiry Date")
                with col4:
                    st.text_input("CVV")
            
            submit = st.form_submit_button("Process Payment")
            if submit:
                st.success("Payment processed successfully!")
    
    with col2:
        st.subheader("Payment Instructions")
        st.info("""
        - Credit Card: Processed instantly
        - Bank Transfer: 2-3 business days
        - Check: 5-7 business days
        """)

# Scholarships Tab
with tabs[2]:
    st.header("Scholarships")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Available Scholarships")
        scholarships = fetch_data(f"{ENDPOINTS['finance']}/scholarships")
        if scholarships and 'results' in scholarships:
            for scholarship in scholarships['results']:
                with st.expander(f"{scholarship['name']} - ${scholarship['amount']:,.2f}"):
                    st.write(f"**Eligibility:** {scholarship['eligibility']}")
                    st.write(f"**Deadline:** {scholarship['deadline']}")
                    st.write(f"**Description:** {scholarship['description']}")
                    if scholarship['status'] == 'OPEN':
                        st.button("Apply Now", key=f"apply_{scholarship['id']}")
    
    with col2:
        st.subheader("My Applications")
        applications = fetch_data(f"{ENDPOINTS['finance']}/scholarship-applications")
        if applications and 'results' in applications:
            for app in applications['results']:
                st.info(f"{app['scholarship_name']} - {app['status']}")

# Financial Aid Tab
with tabs[3]:
    st.header("Financial Aid")
    
    # FAFSA Status
    st.subheader("FAFSA Status")
    fafsa_status = fetch_data(f"{ENDPOINTS['finance']}/fafsa-status")
    if fafsa_status:
        st.info(f"Status: {fafsa_status.get('status', 'Not Submitted')}")
        if fafsa_status.get('missing_documents'):
            st.warning("Missing Documents:")
            for doc in fafsa_status['missing_documents']:
                st.write(f"• {doc}")
    
    # Aid Package
    st.subheader("Financial Aid Package")
    aid_package = fetch_data(f"{ENDPOINTS['finance']}/aid-package")
    if aid_package and 'awards' in aid_package:
        col5, col6 = st.columns(2)
        with col5:
            for award in aid_package['awards']:
                st.metric(
                    award['type'],
                    f"${award['amount']:,.2f}",
                    help=award.get('notes', '')
                )
        with col6:
            st.metric(
                "Total Aid",
                f"${aid_package.get('total_amount', 0):,.2f}"
            )
    
    # Document Upload
    st.subheader("Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload financial documents",
        type=['pdf', 'jpg', 'png']
    )
    if uploaded_file:
        st.success("Document uploaded successfully!")

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Finance Office at finance@university.edu") 