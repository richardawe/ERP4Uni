import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import ENDPOINTS
from utils.api import fetch_data, post_data, update_data
from utils.styles import hide_navigation
from utils.navigation import show_navigation, check_access

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

# Page title
st.title("📚 Library Services")

# Create tabs
tabs = st.tabs(["Book Search", "My Borrowings", "Digital Resources", "Study Rooms"])

# Book Search Tab
with tabs[0]:
    st.subheader("Search Books")
    
    # Search form
    col1, col2 = st.columns(2)
    with col1:
        search_title = st.text_input("Title")
        search_author = st.text_input("Author")
        search_isbn = st.text_input("ISBN")
    with col2:
        category = st.selectbox("Category", ["All", "Science", "Engineering", "Arts", "Business"])
        availability = st.selectbox("Availability", ["All", "Available", "Checked Out"])
    
    if st.button("Search", key="book_search_btn"):
        with st.spinner("Searching books..."):
            # Prepare search parameters
            params = {
                'title': search_title,
                'author': search_author,
                'isbn': search_isbn,
                'category': category if category != "All" else None,
                'availability': availability if availability != "All" else None
            }
            # Remove None values
            params = {k: v for k, v in params.items() if v}
            
            # Fetch books from API
            response = fetch_data(ENDPOINTS['books'], params=params)
            if response and 'results' in response:
                st.dataframe(pd.DataFrame(response['results']))
            else:
                st.info("No books found matching your criteria.")

# My Borrowings Tab
with tabs[1]:
    st.subheader("Current Borrowings")
    with st.spinner("Loading current borrowings..."):
        borrowings = fetch_data(ENDPOINTS['borrowings'], params={'status': 'active'})
        if borrowings and 'results' in borrowings:
            st.dataframe(pd.DataFrame(borrowings['results']))
        else:
            st.info("No current borrowings.")
    
    st.subheader("Borrowing History")
    with st.spinner("Loading borrowing history..."):
        history = fetch_data(ENDPOINTS['borrowings'], params={'status': 'returned'})
        if history and 'results' in history:
            st.dataframe(pd.DataFrame(history['results']))
        else:
            st.info("No borrowing history found.")

# Digital Resources Tab
with tabs[2]:
    st.subheader("E-Books")
    with st.spinner("Loading e-books..."):
        ebooks = fetch_data(ENDPOINTS['ebooks'])
        if ebooks and 'results' in ebooks:
            ebooks_df = pd.DataFrame(ebooks['results'])
            st.dataframe(ebooks_df)
            
            # Download button for each e-book
            if not ebooks_df.empty:
                st.subheader("Download E-Book")
                selected_ebook = st.selectbox("Select E-Book", ebooks_df['Title'].tolist())
                if st.button("Download", key="ebook_download_btn"):
                    # Record download in the database
                    download_data = {
                        'ebook_id': ebooks_df[ebooks_df['Title'] == selected_ebook].iloc[0]['id'],
                        'download_date': datetime.now().isoformat()
                    }
                    response = post_data(f"{ENDPOINTS['ebooks']}/download/", download_data)
                    if response:
                        st.success(f"Started downloading: {selected_ebook}")
                    else:
                        st.error("Failed to initiate download. Please try again.")
        else:
            st.info("No e-books available.")
    
    st.subheader("Online Journals")
    with st.spinner("Loading journals..."):
        journals = fetch_data(ENDPOINTS['journals'])
        if journals and 'results' in journals:
            st.dataframe(pd.DataFrame(journals['results']))
        else:
            st.info("No journals available.")

# Study Rooms Tab
with tabs[3]:
    st.subheader("Book a Study Room")
    
    # First check available rooms
    with st.spinner("Checking room availability..."):
        available_rooms = fetch_data(ENDPOINTS['room_reservations'] + 'available/', 
                                   params={'date': datetime.now().date().isoformat()})
    
    col1, col2 = st.columns(2)
    with col1:
        booking_date = st.date_input("Date", min_value=datetime.now().date())
        time_slots = ["9:00 AM - 11:00 AM", "11:00 AM - 1:00 PM", "2:00 PM - 4:00 PM"]
        time_slot = st.selectbox("Time Slot", time_slots)
    with col2:
        room_types = ["Individual", "Group (2-4)", "Group (5-8)"]
        room_type = st.selectbox("Room Type", room_types)
        durations = ["1 hour", "2 hours", "3 hours"]
        duration = st.selectbox("Duration", durations)
    
    # Check availability for selected criteria
    if st.button("Check Availability", key="check_availability_btn"):
        with st.spinner("Checking availability..."):
            params = {
                'date': booking_date.isoformat(),
                'time_slot': time_slot,
                'room_type': room_type
            }
            available_rooms = fetch_data(ENDPOINTS['room_reservations'] + 'available/', params=params)
            
            if available_rooms and 'results' in available_rooms and available_rooms['results']:
                st.success(f"{len(available_rooms['results'])} rooms available for your criteria!")
                
                # Show available room numbers
                room_numbers = [room['room_number'] for room in available_rooms['results']]
                selected_room = st.selectbox("Select Room", room_numbers)
                
                if st.button("Confirm Booking", key="confirm_booking_btn"):
                    with st.spinner("Processing your booking..."):
                        # Prepare booking data
                        booking_data = {
                            'date': booking_date.isoformat(),
                            'time_slot': time_slot,
                            'room_type': room_type,
                            'duration': duration,
                            'room_number': selected_room,
                            'user_id': st.session_state.user_profile['id'],
                            'user_role': st.session_state.user_profile.get('role', 'student')
                        }
                        
                        # Send booking request to API
                        response = post_data(ENDPOINTS['room_reservations'], booking_data)
                        if response and 'id' in response:
                            st.success(f"Room {selected_room} booked successfully for {booking_date} at {time_slot}!")
                            st.rerun()  # Refresh to update reservations list
                        else:
                            error_msg = response.get('error', 'Unknown error occurred')
                            st.error(f"Failed to book room: {error_msg}")
            else:
                st.warning("No rooms available for your selected criteria. Please try different options.")
    
    st.subheader("Your Reservations")
    with st.spinner("Loading your reservations..."):
        reservations = fetch_data(ENDPOINTS['room_reservations'], 
                                params={'user_id': st.session_state.user_profile['id']})
        if reservations and 'results' in reservations:
            reservations_df = pd.DataFrame(reservations['results'])
            if not reservations_df.empty:
                st.dataframe(reservations_df)
                
                # Cancel reservation option
                st.subheader("Cancel Reservation")
                selected_reservation = st.selectbox(
                    "Select Reservation", 
                    [f"Room {row['room_number']} on {row['date']} at {row['time_slot']}" 
                     for _, row in reservations_df.iterrows()],
                    key="cancel_reservation_select"
                )
                
                if st.button("Cancel Selected Reservation", key="cancel_reservation_btn"):
                    # Get the reservation ID
                    reservation_id = reservations_df.iloc[
                        [f"Room {row['room_number']} on {row['date']} at {row['time_slot']}" == selected_reservation 
                         for _, row in reservations_df.iterrows()]
                    ].iloc[0]['id']
                    
                    # Check cancellation policy
                    booking_date = reservations_df.iloc[
                        [f"Room {row['room_number']} on {row['date']} at {row['time_slot']}" == selected_reservation 
                         for _, row in reservations_df.iterrows()]
                    ].iloc[0]['date']
                    
                    booking_datetime = datetime.strptime(booking_date, '%Y-%m-%d')
                    if (booking_datetime.date() - datetime.now().date()).days < 1:
                        st.error("Reservations can only be cancelled at least 24 hours in advance.")
                    else:
                        with st.spinner("Cancelling reservation..."):
                            response = update_data(
                                f"{ENDPOINTS['room_reservations']}/{reservation_id}/", 
                                {'status': 'cancelled'}
                            )
                            if response:
                                st.success("Reservation cancelled successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to cancel reservation. Please try again.")
            else:
                st.info("No active reservations found.")
        else:
            st.info("No active reservations found.")

# Footer
st.markdown("---")
st.markdown("For assistance, contact library@erp4uni.edu") 