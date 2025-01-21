import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data

# Page config
st.set_page_config(
    page_title="Library Services - ERP4Uni",
    page_icon="📚",
    layout="wide"
)

# Check authentication
if not st.session_state.get('user'):
    st.warning("Please log in to access this page.")
    st.stop()

# Title
st.title("📚 Library Services")

# Create tabs for different sections
tabs = st.tabs(["Book Search", "My Borrowings", "Digital Resources", "Study Rooms"])

# Book Search Tab
with tabs[0]:
    st.header("Book Search")
    
    # Search Form
    with st.form("book_search"):
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("Search by Title, Author, or ISBN")
        with col2:
            category = st.selectbox(
                "Category",
                ["All", "Science", "Technology", "Arts", "Literature", "History"]
            )
        with col3:
            availability = st.selectbox(
                "Availability",
                ["All", "Available", "Checked Out"]
            )
        
        submit = st.form_submit_button("Search")
        if submit:
            # Display search results
            books = fetch_data(f"{ENDPOINTS['library']}/books")
            if books and 'results' in books:
                st.subheader("Search Results")
                for book in books['results']:
                    with st.expander(f"{book['title']} by {book['author']}"):
                        col4, col5 = st.columns([3, 1])
                        with col4:
                            st.write(f"**ISBN:** {book['isbn']}")
                            st.write(f"**Category:** {book['category']}")
                            st.write(f"**Description:** {book['description']}")
                            st.write(f"**Location:** {book['location']}")
                        with col5:
                            st.metric("Copies Available", book['available_copies'])
                            if book['available_copies'] > 0:
                                if st.button("Reserve", key=f"reserve_{book['id']}"):
                                    st.success("Book reserved successfully!")

# My Borrowings Tab
with tabs[1]:
    st.header("My Borrowings")
    
    # Current Borrowings
    st.subheader("Currently Borrowed")
    borrowings = fetch_data(f"{ENDPOINTS['library']}/borrowings")
    if borrowings and 'results' in borrowings:
        for item in borrowings['results']:
            with st.expander(f"{item['title']} (Due: {item['due_date']})"):
                st.write(f"**Borrowed on:** {item['borrow_date']}")
                st.write(f"**Due Date:** {item['due_date']}")
                st.write(f"**Status:** {item['status']}")
                if item['status'] == 'OVERDUE':
                    st.warning(f"Fine: ${item['fine']:.2f}")
                if st.button("Renew", key=f"renew_{item['id']}"):
                    st.success("Book renewed successfully!")
    
    # Borrowing History
    st.subheader("Borrowing History")
    history = fetch_data(f"{ENDPOINTS['library']}/borrowing-history")
    if history and 'results' in history:
        df = pd.DataFrame(history['results'])
        if not df.empty:
            st.dataframe(
                df[['title', 'borrow_date', 'return_date', 'status']],
                hide_index=True
            )

# Digital Resources Tab
with tabs[2]:
    st.header("Digital Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # E-Books
        st.subheader("E-Books")
        ebooks = fetch_data(f"{ENDPOINTS['library']}/ebooks")
        if ebooks and 'results' in ebooks:
            for ebook in ebooks['results']:
                with st.expander(f"{ebook['title']} by {ebook['author']}"):
                    st.write(f"**Format:** {ebook['format']}")
                    st.write(f"**Size:** {ebook['size']}")
                    if st.button("Download", key=f"download_{ebook['id']}"):
                        st.success("E-book download started!")
    
    with col2:
        # Online Journals
        st.subheader("Online Journals")
        journals = fetch_data(f"{ENDPOINTS['library']}/journals")
        if journals and 'results' in journals:
            for journal in journals['results']:
                with st.expander(f"{journal['title']} ({journal['publisher']})"):
                    st.write(f"**Subject:** {journal['subject']}")
                    st.write(f"**Impact Factor:** {journal['impact_factor']}")
                    st.write(f"**Access:** {journal['access_type']}")
                    if st.button("Access Online", key=f"access_{journal['id']}"):
                        st.success("Redirecting to journal website...")

# Study Rooms Tab
with tabs[3]:
    st.header("Study Room Reservations")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Book a Study Room")
        with st.form("room_reservation"):
            date = st.date_input(
                "Date",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=14)
            )
            time_slot = st.selectbox(
                "Time Slot",
                [
                    "8:00 AM - 10:00 AM",
                    "10:00 AM - 12:00 PM",
                    "12:00 PM - 2:00 PM",
                    "2:00 PM - 4:00 PM",
                    "4:00 PM - 6:00 PM",
                    "6:00 PM - 8:00 PM"
                ]
            )
            room_type = st.selectbox(
                "Room Type",
                ["Individual Study", "Group Study (2-4)", "Group Study (5-8)", "Media Room"]
            )
            duration = st.slider(
                "Duration (hours)",
                min_value=1,
                max_value=4,
                value=2
            )
            
            submit = st.form_submit_button("Reserve Room")
            if submit:
                st.success("Room reserved successfully!")
    
    with col2:
        st.subheader("My Reservations")
        reservations = fetch_data(f"{ENDPOINTS['library']}/room-reservations")
        if reservations and 'results' in reservations:
            for reservation in reservations['results']:
                st.info(f"""
                **Date:** {reservation['date']}
                **Time:** {reservation['time_slot']}
                **Room:** {reservation['room_number']}
                **Type:** {reservation['room_type']}
                """)
                if st.button("Cancel", key=f"cancel_{reservation['id']}"):
                    st.success("Reservation cancelled successfully!")

# Footer
st.markdown("---")
st.markdown("Need help? Contact the Library at library@university.edu") 