import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Student Services - ERP4Uni",
    page_icon="👨‍🎓",
    layout="wide"
)

st.title("👨‍🎓 Student Services")

# Tabs for different student services
tabs = st.tabs(["Student Portal", "Library", "Hostel", "Campus Services"])

# Student Portal Tab
with tabs[0]:
    st.header("Student Portal")
    
    # Student Information
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Personal Information")
        st.text("Student ID: STD001")
        st.text("Name: John Doe")
        st.text("Program: Computer Science")
        st.text("Year: 2nd Year")
    
    with col2:
        st.subheader("Academic Status")
        st.metric("GPA", "3.8")
        st.metric("Credits Completed", "60")
        st.metric("Credits Remaining", "60")
    
    # Course Registration
    st.subheader("Course Registration")
    registered_courses = {
        "Course Code": ["CS201", "CS202", "MATH201"],
        "Course Name": ["Data Structures", "Algorithms", "Linear Algebra"],
        "Credits": [3, 3, 3],
        "Schedule": ["Mon/Wed 9:00", "Tue/Thu 10:30", "Fri 14:00"]
    }
    st.dataframe(pd.DataFrame(registered_courses), use_container_width=True)

# Library Tab
with tabs[1]:
    st.header("Library Management")
    
    # Book Search
    st.subheader("Search Books")
    search = st.text_input("Search by title, author, or ISBN")
    
    # Available Books
    st.subheader("Available Books")
    books_data = {
        "Title": ["Python Programming", "Data Science Basics", "Web Development"],
        "Author": ["John Smith", "Sarah Johnson", "Mike Brown"],
        "ISBN": ["123-456-789", "987-654-321", "456-789-123"],
        "Status": ["Available", "Checked Out", "Available"]
    }
    st.dataframe(pd.DataFrame(books_data), use_container_width=True)
    
    # Book Reservation
    st.subheader("Reserve a Book")
    with st.form("book_reservation"):
        book_title = st.selectbox("Select Book", ["Python Programming", "Data Science Basics", "Web Development"])
        reservation_date = st.date_input("Reservation Date")
        submit = st.form_submit_button("Reserve Book")
        if submit:
            st.success(f"Book '{book_title}' reserved successfully!")

# Hostel Tab
with tabs[2]:
    st.header("Hostel Management")
    
    # Room Availability
    st.subheader("Room Availability")
    room_data = {
        "Block": ["A", "B", "C"],
        "Single Rooms": [5, 3, 7],
        "Double Rooms": [10, 8, 12],
        "Total Capacity": [25, 19, 31]
    }
    st.dataframe(pd.DataFrame(room_data), use_container_width=True)
    
    # Room Booking
    st.subheader("Book a Room")
    with st.form("room_booking"):
        block = st.selectbox("Select Block", ["A", "B", "C"])
        room_type = st.selectbox("Room Type", ["Single", "Double"])
        duration = st.selectbox("Duration", ["1 Semester", "2 Semesters", "1 Year"])
        submit = st.form_submit_button("Book Room")
        if submit:
            st.success(f"Room booked successfully in Block {block}!")

# Campus Services Tab
with tabs[3]:
    st.header("Campus Services")
    
    # Service Categories
    services = ["IT Support", "Health Center", "Sports Facilities", "Cafeteria"]
    selected_service = st.selectbox("Select Service", services)
    
    if selected_service == "IT Support":
        st.subheader("IT Support Tickets")
        with st.form("it_support"):
            issue_type = st.selectbox("Issue Type", ["Network", "Software", "Hardware", "Account Access"])
            description = st.text_area("Description")
            priority = st.select_slider("Priority", ["Low", "Medium", "High"])
            submit = st.form_submit_button("Submit Ticket")
            if submit:
                st.success("Support ticket submitted successfully!")
    
    elif selected_service == "Health Center":
        st.subheader("Health Center Appointments")
        with st.form("health_appointment"):
            appointment_type = st.selectbox("Appointment Type", ["General Checkup", "Vaccination", "Consultation"])
            preferred_date = st.date_input("Preferred Date")
            submit = st.form_submit_button("Book Appointment")
            if submit:
                st.success("Appointment booked successfully!")
    
    elif selected_service == "Sports Facilities":
        st.subheader("Sports Facility Booking")
        with st.form("sports_booking"):
            facility = st.selectbox("Select Facility", ["Basketball Court", "Swimming Pool", "Gym", "Tennis Court"])
            booking_date = st.date_input("Booking Date")
            time_slot = st.selectbox("Time Slot", ["Morning", "Afternoon", "Evening"])
            submit = st.form_submit_button("Book Facility")
            if submit:
                st.success(f"{facility} booked successfully!")
    
    else:  # Cafeteria
        st.subheader("Cafeteria Services")
        st.write("Today's Menu")
        menu_data = {
            "Item": ["Breakfast Combo", "Lunch Special", "Dinner Combo"],
            "Description": ["Eggs, Toast, Coffee", "Rice, Curry, Salad", "Pasta, Soup, Dessert"],
            "Price": ["$5", "$8", "$7"]
        }
        st.dataframe(pd.DataFrame(menu_data), use_container_width=True)
