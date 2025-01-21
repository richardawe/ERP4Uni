from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data, get_mock_profile
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access
import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Library Services - ERP4Uni",
    page_icon="📚",
    layout="wide"
)

# Hide default menu
hide_navigation()

# Check access and show navigation
check_access()
show_navigation()

# Initialize user_profile and get user ID safely
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = get_mock_profile('student')

# Get user ID with fallback to default
user_id = st.session_state.user_profile.get('id')
if not user_id:
    st.warning("User profile not properly initialized. Using default profile.")
    st.session_state.user_profile = get_mock_profile('student')
    user_id = st.session_state.user_profile.get('id', '12345')

# Page title
st.title("📚 Library Services")

# Create tabs for different sections
tabs = st.tabs(["Catalog Search", "My Borrowings", "Room Reservations", "Digital Resources"])

# Catalog Search Tab
with tabs[0]:
    st.subheader("Search Library Catalog")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("Search by Title, Author, or ISBN")
        search_type = st.selectbox(
            "Resource Type",
            ["All", "Books", "Journals", "E-Books", "Multimedia"]
        )
    with col2:
        subject = st.selectbox(
            "Subject Area",
            ["All", "Computer Science", "Engineering", "Business", "Arts", "Science"]
        )
        availability = st.selectbox(
            "Availability",
            ["All", "Available Now", "Include Reserved"]
        )
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Relevance", "Title", "Author", "Publication Date"]
        )
        items_per_page = st.selectbox("Items per page", [10, 20, 50])
    
    if st.button("Search", key="search_catalog"):
        with st.spinner("Searching catalog..."):
            search_params = {
                'query': search_query,
                'type': search_type,
                'subject': subject,
                'availability': availability,
                'sort': sort_by,
                'limit': items_per_page
            }
            results = fetch_data('/api/books/', params=search_params)
            
            if results and 'results' in results:
                st.write(f"Found {len(results['results'])} results")
                for item in results['results']:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(item.get('title', 'Unknown Title'))
                            st.write(f"Author: {item.get('author', 'Unknown')}")
                            st.write(f"ISBN: {item.get('isbn', 'N/A')}")
                            st.write(f"Status: {item.get('status', 'Unknown')}")
                        with col2:
                            if item.get('status') == 'Available':
                                if st.button("Reserve", key=f"reserve_{item.get('id', '')}"):
                                    response = post_data('/api/borrowings/', {
                                        'user_id': user_id,
                                        'book_id': item.get('id'),
                                        'date': datetime.now().isoformat()
                                    })
                                    if response and response.get('status') == 'success':
                                        st.success("Book reserved successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to reserve book. Please try again.")
            else:
                st.info("No results found. Try adjusting your search criteria.")

# My Borrowings Tab
with tabs[1]:
    st.subheader("Current Borrowings")
    
    with st.spinner("Loading your borrowings..."):
        borrowings = fetch_data('/api/borrowings/', params={'user_id': user_id})
        if borrowings and 'results' in borrowings:
            current_borrowings = pd.DataFrame(borrowings['results'])
            if not current_borrowings.empty:
                st.dataframe(current_borrowings)
                
                # Renewal section
                st.subheader("Renew Items")
                selected_items = st.multiselect(
                    "Select items to renew",
                    current_borrowings['title'].tolist()
                )
                if selected_items and st.button("Renew Selected Items"):
                    with st.spinner("Processing renewals..."):
                        for item in selected_items:
                            response = update_data('/api/borrowings/renew/', {
                                'user_id': user_id,
                                'book_title': item
                            })
                        st.success("Selected items renewed successfully!")
            else:
                st.info("You have no current borrowings.")

# Room Reservations Tab
with tabs[2]:
    st.subheader("Study Room Reservations")
    
    # Show available rooms
    with st.spinner("Loading available rooms..."):
        rooms = fetch_data('/api/room_reservations/')
        if rooms and 'results' in rooms:
            st.dataframe(pd.DataFrame(rooms['results']))
    
    # Reservation form
    st.subheader("Make a Reservation")
    col1, col2 = st.columns(2)
    with col1:
        room_number = st.selectbox("Room Number", ["101", "102", "103", "201", "202"])
        date = st.date_input("Date")
    with col2:
        start_time = st.time_input("Start Time")
        duration = st.selectbox("Duration (hours)", [1, 2, 3, 4])
    
    if st.button("Reserve Room"):
        if not all([room_number, date, start_time, duration]):
            st.error("Please fill in all required fields.")
        else:
            with st.spinner("Processing reservation..."):
                reservation_data = {
                    'user_id': user_id,
                    'room_number': room_number,
                    'date': date.isoformat(),
                    'start_time': start_time.isoformat(),
                    'duration': duration
                }
                response = post_data('/api/room_reservations/', reservation_data)
                if response and response.get('status') == 'success':
                    st.success("Room reserved successfully!")
                    st.rerun()
                else:
                    st.error("Failed to reserve room. Please try again.")

# Digital Resources Tab
with tabs[3]:
    st.subheader("Digital Resources")
    
    # E-Books section
    st.subheader("E-Books Collection")
    with st.spinner("Loading e-books..."):
        ebooks = fetch_data('/api/ebooks/')
        if ebooks and 'results' in ebooks:
            st.dataframe(pd.DataFrame(ebooks['results']))
    
    # Online Journals section
    st.subheader("Online Journals")
    with st.spinner("Loading journals..."):
        journals = fetch_data('/api/journals/')
        if journals and 'results' in journals:
            for journal in journals['results']:
                with st.expander(journal.get('title', 'Unknown Journal')):
                    st.write(f"Publisher: {journal.get('publisher', 'Unknown')}")
                    st.write(f"Access Level: {journal.get('access_level', 'Unknown')}")
                    if journal.get('access_level') == 'Full':
                        st.link_button("Access Journal", journal.get('url', '#'))
    
    # Research Databases
    st.subheader("Research Databases")
    databases = {
        "JSTOR": "Access to academic journals, books, and primary sources",
        "IEEE Xplore": "Technical literature in engineering and technology",
        "ScienceDirect": "Scientific and medical research articles",
        "ProQuest": "Dissertations, newspapers, and periodicals"
    }
    
    for name, description in databases.items():
        with st.expander(name):
            st.write(description)
            st.link_button(f"Access {name}", "#")

# Footer
st.markdown("---")
st.markdown("Need help? Contact library@erp4uni.edu or visit the Library Information Desk") 