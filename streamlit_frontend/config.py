import os

# API Configuration
API_BASE_URL = "http://localhost:8000/api"
API_TIMEOUT = 5  # seconds

# API Endpoints
ENDPOINTS = {
    # Dashboard
    'stats': f"{API_BASE_URL}/stats/",
    'recent_activities': f"{API_BASE_URL}/recent-activities/",
    
    # Academic
    'departments': f"{API_BASE_URL}/departments/",
    'academic_years': f"{API_BASE_URL}/academic-years/",
    'semesters': f"{API_BASE_URL}/semesters/",
    'courses': f"{API_BASE_URL}/courses/",
    'grades': f"{API_BASE_URL}/grades/",
    'attendance': f"{API_BASE_URL}/attendance/",
    'transcripts': f"{API_BASE_URL}/transcripts/",
    
    # Faculty
    'faculty_profiles': f"{API_BASE_URL}/faculty-profiles/",
    'publications': f"{API_BASE_URL}/publications/",
    'teaching_schedule': f"{API_BASE_URL}/teaching-schedule/",
    'office_hours': f"{API_BASE_URL}/office-hours/",
    
    # Research
    'research_grants': f"{API_BASE_URL}/research-grants/",
    'research_projects': f"{API_BASE_URL}/research-projects/",
    'research_metrics': f"{API_BASE_URL}/research-metrics/",
    
    # Finance
    'finance': f"{API_BASE_URL}/finance/",
    'payments': f"{API_BASE_URL}/payments/",
    'scholarships': f"{API_BASE_URL}/scholarships/",
    'financial_aid': f"{API_BASE_URL}/financial-aid/",
    'transactions': f"{API_BASE_URL}/transactions/",
    
    # Library
    'library': f"{API_BASE_URL}/library/",
    'books': f"{API_BASE_URL}/books/",
    'borrowings': f"{API_BASE_URL}/borrowings/",
    'ebooks': f"{API_BASE_URL}/ebooks/",
    'journals': f"{API_BASE_URL}/journals/",
    'room_reservations': f"{API_BASE_URL}/room-reservations/",
    
    # Housing
    'housing': f"{API_BASE_URL}/housing/",
    'housing_applications': f"{API_BASE_URL}/housing-applications/",
    'maintenance_requests': f"{API_BASE_URL}/maintenance-requests/",
    'room_assignments': f"{API_BASE_URL}/room-assignments/",
    
    # Student Support
    'counseling_appointments': f"{API_BASE_URL}/counseling-appointments/",
    'health_records': f"{API_BASE_URL}/health-records/",
    'fitness_classes': f"{API_BASE_URL}/fitness-classes/",
    'career_services': f"{API_BASE_URL}/career-services/",
    
    # Compliance
    'compliance_reports': f"{API_BASE_URL}/compliance-reports/",
    'audits': f"{API_BASE_URL}/audits/",
    'policies': f"{API_BASE_URL}/policies/",
    
    # Profile
    'profile': f"{API_BASE_URL}/profile",  # For user profile data
} 