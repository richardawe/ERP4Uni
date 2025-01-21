from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Finance & Billing - ERP4Uni",
    page_icon="💰",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Page title
st.title("💰 Finance & Billing")

# Create tabs for different sections
tabs = st.tabs(["Financial Summary", "Payments", "Scholarships", "Financial Aid"])

# Financial Summary Tab
with tabs[0]:
    st.subheader("Financial Overview")
    
    with st.spinner("Loading financial summary..."):
        # Initialize user_profile if not present
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = get_mock_profile('student')
            
        # Fetch financial summary from API
        summary = fetch_data(ENDPOINTS['finance'])
        
        if summary and isinstance(summary.get('results', None), dict):
            data = summary['results']
            
            # Display key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Fees", f"${data.get('total_fees', 0):,.2f}")
                st.metric("Next Payment Due", f"${data.get('next_payment', 0):,.2f}")
            with col2:
                st.metric("Paid Amount", f"${data.get('paid_amount', 0):,.2f}")
                st.metric("Due Date", data.get('due_date', 'Not set'))
            with col3:
                st.metric("Balance Due", f"${data.get('balance_due', 0):,.2f}")
                st.metric("Payment Status", data.get('payment_status', 'Unknown'))
        else:
            st.error("Unable to load financial summary. Please try again later.")
    
    # Transaction History
    st.subheader("Recent Transactions")
    with st.spinner("Loading transactions..."):
        transactions = fetch_data(ENDPOINTS['transactions'])
        if transactions and 'results' in transactions:
            st.dataframe(pd.DataFrame(transactions['results']))
        else:
            st.info("No recent transactions found.")

# Payments Tab
with tabs[1]:
    st.subheader("Make a Payment")
    
    col1, col2 = st.columns(2)
    with col1:
        payment_type = st.selectbox("Payment Type", ["Tuition", "Housing", "Library Fees", "Other"])
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0)
    with col2:
        payment_method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "PayPal"])
        if payment_method == "Credit Card":
            card_number = st.text_input("Card Number")
            col3, col4 = st.columns(2)
            with col3:
                expiry = st.text_input("Expiry Date (MM/YY)")
            with col4:
                cvv = st.text_input("CVV", type="password")
    
    if st.button("Process Payment", key="process_payment_btn"):
        if amount <= 0:
            st.error("Please enter a valid amount.")
        elif payment_method == "Credit Card" and (not card_number or not expiry or not cvv):
            st.error("Please fill in all credit card details.")
        else:
            with st.spinner("Processing payment..."):
                payment_data = {
                    'user_id': st.session_state.user_profile['id'],
                    'payment_type': payment_type,
                    'amount': amount,
                    'payment_method': payment_method,
                    'date': datetime.now().isoformat()
                }
                if payment_method == "Credit Card":
                    payment_data.update({
                        'card_number': card_number,
                        'expiry': expiry,
                        'cvv': cvv
                    })
                
                response = post_data(ENDPOINTS['payments'], payment_data)
                if response and 'id' in response:
                    st.success("Payment processed successfully!")
                    st.rerun()
                else:
                    error_msg = response.get('error', 'Unknown error occurred')
                    st.error(f"Payment failed: {error_msg}")

# Scholarships Tab
with tabs[2]:
    st.subheader("Available Scholarships")
    with st.spinner("Loading scholarships..."):
        scholarships = fetch_data(ENDPOINTS['scholarships'])
        if scholarships and 'results' in scholarships:
            st.dataframe(pd.DataFrame(scholarships['results']))
            
            st.subheader("Apply for Scholarship")
            available_scholarships = [s['name'] for s in scholarships['results'] if s['status'] == 'Open']
            if available_scholarships:
                scholarship = st.selectbox("Select Scholarship", available_scholarships)
                statement = st.text_area("Statement of Purpose")
                uploaded_file = st.file_uploader("Upload Supporting Documents")
                
                if st.button("Submit Application", key="submit_scholarship_btn"):
                    if not statement:
                        st.error("Please provide a statement of purpose.")
                    elif not uploaded_file:
                        st.error("Please upload supporting documents.")
                    else:
                        with st.spinner("Submitting application..."):
                            application_data = {
                                'user_id': st.session_state.user_profile['id'],
                                'scholarship_name': scholarship,
                                'statement': statement,
                                'date_applied': datetime.now().isoformat()
                            }
                            response = post_data(ENDPOINTS['scholarships'] + 'apply/', application_data)
                            if response and 'id' in response:
                                st.success("Application submitted successfully!")
                                st.rerun()
                            else:
                                error_msg = response.get('error', 'Unknown error occurred')
                                st.error(f"Application submission failed: {error_msg}")
            else:
                st.info("No scholarships currently available for application.")
        else:
            st.error("Unable to load scholarships. Please try again later.")

# Financial Aid Tab
with tabs[3]:
    st.subheader("Financial Aid Status")
    
    with st.spinner('Loading financial aid information...'):
        # Initialize user_profile if not present
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = get_mock_profile('student')
            
        aid_info = fetch_data(ENDPOINTS['financial_aid'])
        if aid_info and isinstance(aid_info.get('results', None), dict):
            aid_data = aid_info['results']
            
            # FAFSA Status
            if 'fafsa_status' in aid_data:
                st.subheader('FAFSA Status')
                st.info(aid_data['fafsa_status'])
            
            # Financial Aid Package
            if 'aid_package' in aid_data and isinstance(aid_data['aid_package'], list):
                st.subheader('Financial Aid Package')
                aid_df = pd.DataFrame(aid_data['aid_package'])
                if not aid_df.empty:
                    st.dataframe(aid_df)
                else:
                    st.info("No financial aid package information available.")
            
            # Document Upload Section
            st.subheader('Upload Required Documents')
            doc_type = st.selectbox('Document Type', ['Tax Return', 'Bank Statement', 'Income Verification'])
            uploaded_file = st.file_uploader('Upload Document', type=['pdf', 'jpg', 'png'], key='financial_aid_doc')
            
            if uploaded_file and st.button('Submit Document', key='submit_financial_aid_doc'):
                with st.spinner('Uploading document...'):
                    response = post_data(f"{ENDPOINTS['financial_aid']}/documents", {
                        'doc_type': doc_type,
                        'file': uploaded_file.name
                    })
                    if response and response.get('status') == 'success':
                        st.success('Document uploaded successfully!')
                    else:
                        st.error('Failed to upload document. Please try again.')
        else:
            st.error("Unable to load financial aid information. Please try again later.")

# Footer
st.markdown("---")
st.markdown("Need help? Contact finance@erp4uni.edu or visit the Finance Office") 