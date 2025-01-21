def get_mock_profile(role='student'):
    """Generate mock user profile data"""
    profiles = {
        'student': {
            'id': '12345',
            'name': 'John Doe',
            'role': 'student',
            'email': 'john.doe@university.edu',
            'department': 'Computer Science',
            'year': '3rd Year',
            'student_id': 'STU123456'
        },
        'faculty': {
            'id': '67890',
            'name': 'Dr. Jane Smith',
            'role': 'faculty',
            'email': 'jane.smith@university.edu',
            'department': 'Computer Science',
            'position': 'Associate Professor',
            'faculty_id': 'FAC789012'
        },
        'admin': {
            'id': '11111',
            'name': 'Admin User',
            'role': 'admin',
            'email': 'admin@university.edu',
            'department': 'Administration',
            'admin_id': 'ADM111111'
        }
    }
    return profiles.get(role, profiles['student'])

def get_mock_financial_data():
    """Generate mock financial data"""
    return {
        'results': {
            'total_fees': 25000.00,
            'paid_amount': 15000.00,
            'balance_due': 10000.00,
            'next_payment': 5000.00,
            'due_date': '2024-05-01',
            'payment_status': 'Partially Paid'
        }
    }

def get_mock_transactions():
    """Generate mock transaction history"""
    return {
        'results': [
            {
                'date': '2024-03-15',
                'description': 'Tuition Payment',
                'amount': 5000.00,
                'type': 'Credit',
                'status': 'Completed'
            },
            {
                'date': '2024-02-15',
                'description': 'Library Fine',
                'amount': 25.00,
                'type': 'Debit',
                'status': 'Completed'
            },
            {
                'date': '2024-01-15',
                'description': 'Tuition Payment',
                'amount': 5000.00,
                'type': 'Credit',
                'status': 'Completed'
            }
        ]
    }

def get_mock_books():
    """Generate mock book catalog data"""
    return {
        'results': [
            {
                'id': 'B001',
                'title': 'Introduction to Computer Science',
                'author': 'Dr. Alan Smith',
                'isbn': '978-0-123456-78-9',
                'status': 'Available',
                'subject': 'Computer Science'
            },
            {
                'id': 'B002',
                'title': 'Advanced Database Systems',
                'author': 'Prof. Maria Garcia',
                'isbn': '978-0-234567-89-0',
                'status': 'Available',
                'subject': 'Computer Science'
            },
            {
                'id': 'B003',
                'title': 'Modern Web Development',
                'author': 'James Wilson',
                'isbn': '978-0-345678-90-1',
                'status': 'Reserved',
                'subject': 'Computer Science'
            }
        ]
    }

def get_mock_borrowings(user_id=None):
    """Generate mock borrowing data"""
    return {
        'results': [
            {
                'id': 'BR001',
                'title': 'Data Structures and Algorithms',
                'due_date': '2024-04-15',
                'status': 'Active',
                'renewable': True
            },
            {
                'id': 'BR002',
                'title': 'Software Engineering Principles',
                'due_date': '2024-04-10',
                'status': 'Active',
                'renewable': True
            }
        ]
    }

def get_mock_room_reservations():
    """Generate mock study room reservation data"""
    return {
        'results': [
            {
                'room_number': '101',
                'capacity': 4,
                'features': ['Whiteboard', 'Monitor'],
                'availability': 'Available'
            },
            {
                'room_number': '102',
                'capacity': 6,
                'features': ['Whiteboard', 'Monitor', 'Conference Phone'],
                'availability': 'Available'
            },
            {
                'room_number': '201',
                'capacity': 8,
                'features': ['Whiteboard', 'Projector', 'Conference System'],
                'availability': 'Reserved'
            }
        ]
    }

def get_mock_ebooks():
    """Generate mock e-book data"""
    return {
        'results': [
            {
                'id': 'E001',
                'title': 'Cloud Computing Fundamentals',
                'author': 'Dr. Sarah Johnson',
                'format': 'PDF',
                'subject': 'Computer Science'
            },
            {
                'id': 'E002',
                'title': 'Artificial Intelligence: A Modern Approach',
                'author': 'Prof. Michael Brown',
                'format': 'EPUB',
                'subject': 'Computer Science'
            }
        ]
    }

def get_mock_journals():
    """Generate mock journal data"""
    return {
        'results': [
            {
                'title': 'Journal of Computer Science',
                'publisher': 'Tech Publications',
                'access_level': 'Full',
                'url': 'https://example.com/jcs'
            },
            {
                'title': 'International Journal of Software Engineering',
                'publisher': 'Engineering Press',
                'access_level': 'Full',
                'url': 'https://example.com/ijse'
            }
        ]
    } 