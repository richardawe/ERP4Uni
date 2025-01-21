from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Department, AcademicYear, Semester, Course, FacultyProfile, Publication,
    ResearchGrant, ResearchProject, LibraryResource, LibraryBorrowing,
    Housing, HousingApplication, CounselingAppointment, HealthRecord,
    FitnessClass, ComplianceReport, Audit
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_head_name(self, obj):
        return obj.head.get_full_name() if obj.head else None

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    academic_year_display = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = '__all__'

    def get_academic_year_display(self, obj):
        return str(obj.academic_year)

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_department_name(self, obj):
        return obj.department.name

    def get_instructor_name(self, obj):
        return obj.instructor.get_full_name() if obj.instructor else None

class FacultyProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = FacultyProfile
        fields = '__all__'

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

class PublicationSerializer(serializers.ModelSerializer):
    faculty_name = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = '__all__'

    def get_faculty_name(self, obj):
        return obj.faculty.user.get_full_name()

class ResearchGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGrant
        fields = '__all__'

class ResearchProjectSerializer(serializers.ModelSerializer):
    principal_investigator_name = serializers.SerializerMethodField()
    co_investigators_names = serializers.SerializerMethodField()

    class Meta:
        model = ResearchProject
        fields = '__all__'

    def get_principal_investigator_name(self, obj):
        return obj.principal_investigator.user.get_full_name()

    def get_co_investigators_names(self, obj):
        return [inv.user.get_full_name() for inv in obj.co_investigators.all()]

class LibraryResourceSerializer(serializers.ModelSerializer):
    availability_status = serializers.SerializerMethodField()

    class Meta:
        model = LibraryResource
        fields = '__all__'

    def get_availability_status(self, obj):
        return "Available" if obj.available_copies > 0 else "Checked Out"

class LibraryBorrowingSerializer(serializers.ModelSerializer):
    resource_details = LibraryResourceSerializer(source='resource', read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = LibraryBorrowing
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.get_full_name()

class HousingSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Housing
        fields = '__all__'

    def get_availability(self, obj):
        available = obj.capacity - obj.occupied
        if available == 0:
            return "Full"
        elif available <= 2:
            return "Limited"
        return "Available"

class HousingApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    semester_display = serializers.SerializerMethodField()

    class Meta:
        model = HousingApplication
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.get_full_name()

    def get_semester_display(self, obj):
        return str(obj.semester)

class CounselingAppointmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    counselor_name = serializers.SerializerMethodField()

    class Meta:
        model = CounselingAppointment
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.get_full_name()

    def get_counselor_name(self, obj):
        return obj.counselor.get_full_name()

class HealthRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = HealthRecord
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.get_full_name()

class FitnessClassSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_availability(self, obj):
        return obj.capacity - obj.enrolled

class ComplianceReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceReport
        fields = '__all__'

    def get_generated_by_name(self, obj):
        return obj.generated_by.get_full_name()

class AuditSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Audit
        fields = '__all__'

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.name 