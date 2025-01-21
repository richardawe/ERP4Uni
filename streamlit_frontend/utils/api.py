import requests
from typing import Dict, Any, Optional, List
from config import API_TIMEOUT
import random
from datetime import datetime, timedelta
import streamlit as st
from .mock_data import (
    get_mock_profile, get_mock_financial_data, get_mock_transactions,
    get_mock_books, get_mock_borrowings, get_mock_room_reservations,
    get_mock_ebooks, get_mock_journals
)

# Define user roles and their module access
ROLE_ACCESS = {
    'student': {
        'modules': [
            'Academic Records',
            'Library Services',
            'Finance & Billing',
            'Housing Management',
            'Student Support',
            'Campus Life'
        ],
        'description': 'Student access to academic and campus services'
    },
    'lecturer': {
        'modules': [
            'Faculty Portal',
            'Research Management',
            'Library Services',
            'Academic Records',
            'Campus Life'
        ],
        'description': 'Faculty access to teaching and research tools'
    },
    'admin': {
        'modules': [
            'Academic Records',
            'Faculty Portal',
            'Research Management',
            'Finance & Billing',
            'Compliance & Reports',
            'Housing Management',
            'Library Services',
            'Student Support',
            'Campus Life'
        ],
        'description': 'Administrative access to all modules'
    }
}

def get_headers() -> Dict[str, str]:
    """Get headers for API requests including authentication token."""
    headers = {
        'Content-Type': 'application/json'
    }
    if 'auth_token' in st.session_state:
        headers['Authorization'] = f"Token {st.session_state.auth_token}"
    return headers

def get_mock_data(endpoint: str) -> Dict[str, Any]:
    """Return mock data based on the endpoint."""
    
    # Mock data for financial summary
    if 'finance' in endpoint:
        return {
            'results': {
                'total_fees': 12500.00,
                'next_payment': 2500.00,
                'paid_amount': 7500.00,
                'due_date': '2024-03-15',
                'balance_due': 5000.00,
                'payment_status': 'On Track'
            }
        }
    
    # Mock data for transactions
    elif 'transactions' in endpoint:
        return {
            'results': [
                {
                    'date': '2024-01-15',
                    'description': 'Spring Semester Fee',
                    'amount': 5000.00,
                    'status': 'Completed'
                },
                {
                    'date': '2024-01-01',
                    'description': 'Housing Payment',
                    'amount': 2000.00,
                    'status': 'Completed'
                },
                {
                    'date': '2023-12-15',
                    'description': 'Library Fine',
                    'amount': 25.00,
                    'status': 'Pending'
                }
            ]
        }
    
    # Mock data for payments
    elif 'payments' in endpoint:
        return {
            'id': 1,
            'status': 'success',
            'message': 'Payment processed successfully'
        }
    
    # Mock data for scholarships
    elif 'scholarships' in endpoint:
        if 'apply' in endpoint:
            return {
                'id': 1,
                'status': 'success',
                'message': 'Application submitted successfully'
            }
        return {
            'results': [
                {
                    'name': 'Merit Scholarship',
                    'amount': 5000.00,
                    'deadline': '2024-03-15',
                    'status': 'Open'
                },
                {
                    'name': 'Sports Excellence',
                    'amount': 3000.00,
                    'deadline': '2024-04-01',
                    'status': 'Open'
                },
                {
                    'name': 'Research Grant',
                    'amount': 2500.00,
                    'deadline': '2024-03-30',
                    'status': 'Closed'
                }
            ]
        }
    
    # Mock data for financial aid
    elif 'financial-aid' in endpoint:
        if 'documents' in endpoint:
            return {
                'id': 1,
                'status': 'success',
                'message': 'Documents uploaded successfully'
            }
        return {
            'results': {
                'fafsa_status': 'Submitted - Under Review',
                'aid_package': [
                    {
                        'type': 'Federal Grant',
                        'amount': 5500.00,
                        'status': 'Approved'
                    },
                    {
                        'type': 'State Grant',
                        'amount': 2000.00,
                        'status': 'Pending'
                    },
                    {
                        'type': 'Work Study',
                        'amount': 3000.00,
                        'status': 'Available'
                    }
                ]
            }
        }
    
    # Add other mock data cases here
    
    return {'results': []}

def has_module_access(user_role: str, module_name: str) -> bool:
    """Check if a user role has access to a specific module"""
    if user_role not in ROLE_ACCESS:
        return False
    return module_name in ROLE_ACCESS[user_role]['modules']

def fetch_data(endpoint, params=None):
    """
    Fetch data from the API endpoint
    For now, returns mock data for testing
    """
    # Initialize params if None
    params = params or {}
    
    # Mock responses based on endpoint
    if endpoint == '/api/finance/summary/':
        return get_mock_financial_data()
    elif endpoint == '/api/finance/transactions/':
        return get_mock_transactions()
    elif endpoint == '/api/scholarships/':
        return {
            'results': [
                {
                    'name': 'Merit Scholarship',
                    'amount': 5000.00,
                    'deadline': '2024-03-15',
                    'status': 'Open'
                },
                {
                    'name': 'Sports Excellence',
                    'amount': 3000.00,
                    'deadline': '2024-04-01',
                    'status': 'Open'
                },
                {
                    'name': 'Research Grant',
                    'amount': 2500.00,
                    'deadline': '2024-03-30',
                    'status': 'Closed'
                }
            ]
        }
    elif endpoint == '/api/financial-aid/':
        return {
            'results': {
                'fafsa_status': 'Submitted - Under Review',
                'aid_package': [
                    {
                        'type': 'Federal Grant',
                        'amount': 5500.00,
                        'status': 'Approved'
                    },
                    {
                        'type': 'State Grant',
                        'amount': 2000.00,
                        'status': 'Pending'
                    },
                    {
                        'type': 'Work Study',
                        'amount': 3000.00,
                        'status': 'Available'
                    }
                ]
            }
        }
    elif endpoint == '/api/books/':
        return get_mock_books()
    elif endpoint == '/api/borrowings/':
        # Get user_id from params or session state
        user_id = params.get('user_id')
        if not user_id and 'user_profile' in st.session_state:
            user_id = st.session_state.user_profile.get('id', '12345')
        return get_mock_borrowings(user_id)
    elif endpoint == '/api/room_reservations/':
        return get_mock_room_reservations()
    elif endpoint == '/api/ebooks/':
        return get_mock_ebooks()
    elif endpoint == '/api/journals/':
        return get_mock_journals()
    
    # Default response
    return {'results': {}}

def post_data(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Post data to the API with error handling and mock response."""
    try:
        # For development, return mock success response
        return get_mock_data(url)
        
        # For production, uncomment the following:
        # response = requests.post(url, headers=get_headers(), json=data, timeout=5)
        # response.raise_for_status()
        # return response.json()
    except Exception as e:
        print(f"Error posting data: {str(e)}")
        return {'error': str(e)}

def update_data(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update data via the API with error handling and mock response."""
    try:
        # For development, return mock success response
        return get_mock_data(url)
        
        # For production, uncomment the following:
        # response = requests.put(url, headers=get_headers(), json=data, timeout=5)
        # response.raise_for_status()
        # return response.json()
    except Exception as e:
        print(f"Error updating data: {str(e)}")
        return {'error': str(e)}

def delete_data(url: str) -> Dict[str, Any]:
    """Delete data at API endpoint"""
    try:
        response = requests.delete(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return {'success': True}
    except requests.exceptions.RequestException as e:
        print(f"Error deleting data at {url}: {str(e)}")
        return {'error': str(e), 'success': False} 