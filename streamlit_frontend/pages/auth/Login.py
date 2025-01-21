import streamlit as st
import os
from config import ENDPOINTS
from utils.api import post_data

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None

# Page config
st.set_page_config(
    page_title="Login - ERP4Uni",
    page_icon="🔐",
    layout="centered"
)

# Title
st.title("🔐 Login")

# Show current login status
if st.session_state.user:
    st.success(f"Logged in as: {st.session_state.user.get('full_name', st.session_state.user.get('username'))}")
    if st.button("Logout"):
        # Clear token and user info
        st.session_state.token = None
        st.session_state.user = None
        if 'ERP_AUTH_TOKEN' in os.environ:
            del os.environ['ERP_AUTH_TOKEN']
        st.experimental_rerun()
else:
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username and password:
                response = post_data(ENDPOINTS['login'], {
                    'username': username,
                    'password': password
                })
                
                if response and 'token' in response:
                    # Save token to environment variable and session state
                    token = response['token']
                    os.environ['ERP_AUTH_TOKEN'] = token
                    st.session_state.token = token
                    
                    # Save user info in session state
                    st.session_state.user = {
                        'id': response['user_id'],
                        'username': response['username'],
                        'email': response['email'],
                        'full_name': response['full_name']
                    }
                    
                    st.success("Login successful! You can now access all features.")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password") 