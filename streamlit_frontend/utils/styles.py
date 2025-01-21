import streamlit as st

def hide_navigation():
    """Hide default Streamlit navigation menu and adjust layout"""
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            div[data-testid='stSidebarNav'] {display: none;}
            div.block-container {padding-top: 2rem;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True) 