import streamlit as st
import pandas as pd
from datetime import datetime
from config import ENDPOINTS
from utils.api import fetch_data, post_data

def render_financial_summary():
    st.subheader("Financial Summary")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Fees", "$12,000")
        st.metric("Paid Amount", "$8,000")
    with col2:
        st.metric("Balance Due", "$4,000")
        st.metric("Next Payment", "$2,000")
    with col3:
        st.metric("Due Date", "Feb 15, 2025")
        st.metric("Payment Status", "On Track")
    
    # Transaction history
    st.subheader("Recent Transactions")
    transactions = pd.DataFrame({
        'Date': ['2025-01-15', '2024-12-20', '2024-11-15'],
        'Description': ['Spring 2025 Tuition', 'Library Fine', 'Fall 2024 Tuition'],
        'Amount': ['$2,000', '$50', '$2,000'],
        'Status': ['Paid', 'Pending', 'Paid']
    })
    st.dataframe(transactions)

def render_payments():
    st.subheader("Make a Payment")
    
    with st.form("payment_form"):
        payment_type = st.selectbox(
            "Payment Type",
            ["Tuition Fee", "Library Fine", "Hostel Fee", "Other Charges"]
        )
        
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        
        payment_method = st.selectbox(
            "Payment Method",
            ["Credit Card", "Bank Transfer", "PayPal"]
        )
        
        if payment_method == "Credit Card":
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Card Number")
                st.text_input("Cardholder Name")
            with col2:
                st.text_input("Expiry Date")
                st.text_input("CVV", type="password")
        
        submitted = st.form_submit_button("Process Payment")
        if submitted and amount > 0:
            st.success(f"Payment of ${amount:.2f} processed successfully!")

def render_scholarships():
    st.subheader("Scholarships & Financial Aid")
    
    # Available scholarships
    st.write("Available Scholarships")
    scholarships = pd.DataFrame({
        'Name': ['Merit Scholarship', 'Need-based Grant', 'Sports Excellence'],
        'Amount': ['$5,000', '$3,000', '$2,000'],
        'Deadline': ['2025-03-01', '2025-02-15', '2025-02-28'],
        'Status': ['Open', 'Open', 'Closed']
    })
    st.dataframe(scholarships)
    
    # Application form
    st.subheader("Apply for Scholarship")
    with st.form("scholarship_form"):
        scholarship = st.selectbox(
            "Select Scholarship",
            ["Merit Scholarship", "Need-based Grant"]
        )
        
        st.text_area("Statement of Need")
        documents = st.file_uploader("Supporting Documents", type=["pdf"], accept_multiple_files=True)
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            st.success("Scholarship application submitted successfully!")

# Main page content
st.title("💰 Finance & Billing")

# Create tabs for different functions
tabs = st.tabs(["Financial Summary", "Make Payment", "Scholarships"])

with tabs[0]:
    render_financial_summary()

with tabs[1]:
    render_payments()

with tabs[2]:
    render_scholarships() 