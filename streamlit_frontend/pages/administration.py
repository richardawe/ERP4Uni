import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Administration - ERP4Uni",
    page_icon="👨‍💼",
    layout="wide"
)

st.title("👨‍💼 Administration")

# Tabs for different administrative functions
tabs = st.tabs(["Admissions", "Finance", "HR", "Assets"])

# Admissions Tab
with tabs[0]:
    st.header("Admissions Management")
    
    # Application Status Overview
    st.subheader("Application Status")
    status_data = {
        "Status": ["Pending", "Under Review", "Accepted", "Rejected"],
        "Count": [45, 30, 80, 20]
    }
    status_df = pd.DataFrame(status_data)
    st.bar_chart(status_df.set_index("Status"))
    
    # Applications List
    st.subheader("Recent Applications")
    applications_data = {
        "ID": ["A001", "A002", "A003"],
        "Name": ["John Doe", "Jane Smith", "Bob Johnson"],
        "Program": ["Computer Science", "Engineering", "Business"],
        "Status": ["Under Review", "Accepted", "Pending"],
        "Date": ["2024-01-15", "2024-01-16", "2024-01-17"]
    }
    applications_df = pd.DataFrame(applications_data)
    st.dataframe(applications_df, use_container_width=True)

# Finance Tab
with tabs[1]:
    st.header("Finance Management")
    
    # Financial Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", "$1.2M", "+12%")
    with col2:
        st.metric("Expenses", "$800K", "+5%")
    with col3:
        st.metric("Net Income", "$400K", "+20%")
    
    # Transactions
    st.subheader("Recent Transactions")
    transactions_data = {
        "Date": ["2024-01-15", "2024-01-16", "2024-01-17"],
        "Description": ["Tuition Fee", "Faculty Salary", "Equipment Purchase"],
        "Type": ["Income", "Expense", "Expense"],
        "Amount": ["$5000", "$3000", "$2000"]
    }
    transactions_df = pd.DataFrame(transactions_data)
    st.dataframe(transactions_df, use_container_width=True)
    
    # Add New Transaction
    st.subheader("Add New Transaction")
    with st.form("new_transaction_form"):
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0)
        trans_type = st.selectbox("Type", ["Income", "Expense"])
        
        submit = st.form_submit_button("Add Transaction")
        if submit:
            st.success("Transaction added successfully!")

# HR Tab
with tabs[2]:
    st.header("Human Resources")
    
    # Employee Directory
    st.subheader("Employee Directory")
    employee_data = {
        "ID": ["E001", "E002", "E003"],
        "Name": ["Alice Brown", "Charlie Davis", "Eve Wilson"],
        "Department": ["Administration", "IT", "Finance"],
        "Position": ["HR Manager", "System Admin", "Accountant"]
    }
    employee_df = pd.DataFrame(employee_data)
    st.dataframe(employee_df, use_container_width=True)
    
    # Add New Employee
    st.subheader("Add New Employee")
    with st.form("new_employee_form"):
        name = st.text_input("Full Name")
        department = st.selectbox("Department", ["Administration", "IT", "Finance"])
        position = st.text_input("Position")
        
        submit = st.form_submit_button("Add Employee")
        if submit:
            st.success(f"Employee {name} added successfully!")

# Assets Tab
with tabs[3]:
    st.header("Asset Management")
    
    # Asset Overview
    st.subheader("Asset Inventory")
    asset_data = {
        "Asset ID": ["AST001", "AST002", "AST003"],
        "Name": ["Computers", "Lab Equipment", "Furniture"],
        "Quantity": [100, 50, 200],
        "Value": ["$100,000", "$75,000", "$50,000"]
    }
    asset_df = pd.DataFrame(asset_data)
    st.dataframe(asset_df, use_container_width=True)
    
    # Add New Asset
    st.subheader("Add New Asset")
    with st.form("new_asset_form"):
        asset_name = st.text_input("Asset Name")
        quantity = st.number_input("Quantity", min_value=1)
        value = st.number_input("Value ($)", min_value=0.0)
        
        submit = st.form_submit_button("Add Asset")
        if submit:
            st.success(f"Asset {asset_name} added successfully!")
