from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import User
from .models import (
    Department, AcademicYear, Semester, Course, FacultyProfile, Publication,
    ResearchGrant, ResearchProject, LibraryResource, LibraryBorrowing,
    Housing, HousingApplication, CounselingAppointment, HealthRecord,
    FitnessClass, ComplianceReport, Audit
)
from .serializers import (
    UserSerializer, DepartmentSerializer, AcademicYearSerializer,
    SemesterSerializer, CourseSerializer, FacultyProfileSerializer,
    PublicationSerializer, ResearchGrantSerializer, ResearchProjectSerializer,
    LibraryResourceSerializer, LibraryBorrowingSerializer, HousingSerializer,
    HousingApplicationSerializer, CounselingAppointmentSerializer,
    HealthRecordSerializer, FitnessClassSerializer, ComplianceReportSerializer,
    AuditSerializer
)

User = get_user_model()

# Create your views here.

# Base ViewSet with common functionality
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class AcademicYearViewSet(BaseViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

class SemesterViewSet(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__code=department)
        return queryset

class FacultyProfileViewSet(BaseViewSet):
    queryset = FacultyProfile.objects.all()
    serializer_class = FacultyProfileSerializer

    def get_queryset(self):
        queryset = FacultyProfile.objects.all()
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__code=department)
        return queryset

class PublicationViewSet(BaseViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def get_queryset(self):
        queryset = Publication.objects.all()
        faculty = self.request.query_params.get('faculty', None)
        if faculty:
            queryset = queryset.filter(faculty__user__id=faculty)
        return queryset

class ResearchGrantViewSet(BaseViewSet):
    queryset = ResearchGrant.objects.all()
    serializer_class = ResearchGrantSerializer

    def get_queryset(self):
        queryset = ResearchGrant.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class ResearchProjectViewSet(BaseViewSet):
    queryset = ResearchProject.objects.all()
    serializer_class = ResearchProjectSerializer

    def get_queryset(self):
        queryset = ResearchProject.objects.all()
        status = self.request.query_params.get('status', None)
        investigator = self.request.query_params.get('investigator', None)
        if status:
            queryset = queryset.filter(status=status)
        if investigator:
            queryset = queryset.filter(
                Q(principal_investigator__user__id=investigator) |
                Q(co_investigators__user__id=investigator)
            ).distinct()
        return queryset

class LibraryResourceViewSet(BaseViewSet):
    queryset = LibraryResource.objects.all()
    serializer_class = LibraryResourceSerializer

    def get_queryset(self):
        queryset = LibraryResource.objects.all()
        resource_type = self.request.query_params.get('type', None)
        available = self.request.query_params.get('available', None)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if available:
            queryset = queryset.filter(available_copies__gt=0)
        return queryset

class LibraryBorrowingViewSet(BaseViewSet):
    queryset = LibraryBorrowing.objects.all()
    serializer_class = LibraryBorrowingSerializer

    def get_queryset(self):
        queryset = LibraryBorrowing.objects.all()
        user = self.request.query_params.get('user', None)
        if user:
            queryset = queryset.filter(user__id=user)
        return queryset

class HousingViewSet(BaseViewSet):
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer

    def get_queryset(self):
        queryset = Housing.objects.all()
        room_type = self.request.query_params.get('room_type', None)
        available = self.request.query_params.get('available', None)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if available:
            queryset = queryset.filter(occupied__lt=models.F('capacity'))
        return queryset

class HousingApplicationViewSet(BaseViewSet):
    queryset = HousingApplication.objects.all()
    serializer_class = HousingApplicationSerializer

    def get_queryset(self):
        queryset = HousingApplication.objects.all()
        status = self.request.query_params.get('status', None)
        student = self.request.query_params.get('student', None)
        if status:
            queryset = queryset.filter(status=status)
        if student:
            queryset = queryset.filter(student__id=student)
        return queryset

class CounselingAppointmentViewSet(BaseViewSet):
    queryset = CounselingAppointment.objects.all()
    serializer_class = CounselingAppointmentSerializer

    def get_queryset(self):
        queryset = CounselingAppointment.objects.all()
        student = self.request.query_params.get('student', None)
        counselor = self.request.query_params.get('counselor', None)
        if student:
            queryset = queryset.filter(student__id=student)
        if counselor:
            queryset = queryset.filter(counselor__id=counselor)
        return queryset

class HealthRecordViewSet(BaseViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

    def get_queryset(self):
        queryset = HealthRecord.objects.all()
        student = self.request.query_params.get('student', None)
        if student:
            queryset = queryset.filter(student__id=student)
        return queryset

class FitnessClassViewSet(BaseViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        queryset = FitnessClass.objects.all()
        available = self.request.query_params.get('available', None)
        if available:
            queryset = queryset.filter(enrolled__lt=models.F('capacity'))
        return queryset

class ComplianceReportViewSet(BaseViewSet):
    queryset = ComplianceReport.objects.all()
    serializer_class = ComplianceReportSerializer

    def get_queryset(self):
        queryset = ComplianceReport.objects.all()
        report_type = self.request.query_params.get('type', None)
        status = self.request.query_params.get('status', None)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class AuditViewSet(BaseViewSet):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

    def get_queryset(self):
        queryset = Audit.objects.all()
        status = self.request.query_params.get('status', None)
        department = self.request.query_params.get('department', None)
        if status:
            queryset = queryset.filter(status=status)
        if department:
            queryset = queryset.filter(assigned_to__code=department)
        return queryset

# Additional API endpoints for dashboard statistics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get statistics for the dashboard"""
    try:
        # Get total students (handle case where Students group doesn't exist)
        try:
            total_students = User.objects.filter(groups__name='Students').count()
        except:
            total_students = 0
        
        # Get housing occupancy with safe aggregation
        try:
            housing_stats = Housing.objects.aggregate(
                total_capacity=Sum('capacity') or 0,
                total_occupied=Sum('occupied') or 0
            )
            housing_occupancy = {
                'total_capacity': housing_stats.get('total_capacity', 0),
                'total_occupied': housing_stats.get('total_occupied', 0)
            }
        except Exception:
            housing_occupancy = {'total_capacity': 0, 'total_occupied': 0}
        
        # Build stats dictionary with safe counts and handle potential None values
        stats = {
            'total_students': total_students,
            'total_faculty': FacultyProfile.objects.count() or 0,
            'total_departments': Department.objects.count() or 0,
            'active_courses': Course.objects.filter(semester__is_active=True).count() or 0,
            'library_resources': LibraryResource.objects.count() or 0,
            'housing_occupancy': housing_occupancy,
            'research_projects': ResearchProject.objects.filter(status='IN_PROGRESS').count() or 0,
            'compliance_score': ComplianceReport.objects.filter(status='APPROVED').count() or 0,
        }
        return Response(stats)
    except Exception as e:
        # Return a response with default values in case of error
        default_stats = {
            'total_students': 0,
            'total_faculty': 0,
            'total_departments': 0,
            'active_courses': 0,
            'library_resources': 0,
            'housing_occupancy': {'total_capacity': 0, 'total_occupied': 0},
            'research_projects': 0,
            'compliance_score': 0,
            'error': str(e)
        }
        return Response(default_stats, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_activities(request):
    """Get recent activities across all modules"""
    try:
        activities = []
        
        # Add recent library borrowings
        try:
            borrowings = LibraryBorrowing.objects.order_by('-borrow_date')[:5]
            for b in borrowings:
                activities.append({
                    'type': 'library',
                    'description': f"{b.user.get_full_name()} borrowed {b.resource.title}",
                    'date': b.borrow_date.isoformat()
                })
        except Exception:
            pass
        
        # Add recent housing applications
        try:
            applications = HousingApplication.objects.order_by('-created_at')[:5]
            for a in applications:
                activities.append({
                    'type': 'housing',
                    'description': f"New housing application from {a.student.get_full_name()}",
                    'date': a.created_at.isoformat()
                })
        except Exception:
            pass
        
        # Add recent counseling appointments
        try:
            appointments = CounselingAppointment.objects.order_by('-date')[:5]
            for a in appointments:
                activities.append({
                    'type': 'counseling',
                    'description': f"Counseling session scheduled for {a.student.get_full_name()}",
                    'date': a.date.isoformat()
                })
        except Exception:
            pass
        
        # Sort all activities by date
        activities.sort(key=lambda x: x['date'], reverse=True)
        return Response({'activities': activities[:10]})
    except Exception as e:
        return Response(
            {'activities': [], 'error': str(e)},
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """Handle user login and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                      status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'},
                      status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username
    })
