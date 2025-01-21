from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    created and modified fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    """
    Custom user model for the ERP system
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='department_head')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

def get_default_end_date():
    return datetime.date.today() + datetime.timedelta(days=365)

class AcademicYear(models.Model):
    year = models.CharField(max_length=9, default='2024-2025')  # Format: 2024-2025
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=get_default_end_date)

    def __str__(self):
        return self.year

class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('FALL', 'Fall'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
    ]
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=6, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.academic_year}"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.IntegerField()
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    joining_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

class Publication(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    journal = models.CharField(max_length=200)
    publication_date = models.DateField()
    doi = models.CharField(max_length=100, blank=True)
    citation_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class ResearchGrant(models.Model):
    GRANT_STATUS = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('UNDER_REVIEW', 'Under Review'),
        ('AWARDED', 'Awarded'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=12, choices=GRANT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ResearchProject(models.Model):
    PROJECT_STATUS = [
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]
    title = models.CharField(max_length=200)
    principal_investigator = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    co_investigators = models.ManyToManyField(FacultyProfile, related_name='co_investigator_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=12, choices=PROJECT_STATUS)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class LibraryResource(models.Model):
    RESOURCE_TYPE = [
        ('BOOK', 'Book'),
        ('EBOOK', 'E-Book'),
        ('JOURNAL', 'Journal'),
        ('ARTICLE', 'Article'),
        ('MULTIMEDIA', 'Multimedia'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE)
    isbn = models.CharField(max_length=13, blank=True)
    location = models.CharField(max_length=100)
    available_copies = models.IntegerField(default=1)
    total_copies = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title

class LibraryBorrowing(models.Model):
    resource = models.ForeignKey(LibraryResource, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    renewals = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"

class Housing(models.Model):
    ROOM_TYPE = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    ]
    building = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    semester_fee = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.building} - {self.room_number}"

class HousingApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preferred_building = models.CharField(max_length=100)
    room_type = models.CharField(max_length=10, choices=Housing.ROOM_TYPE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    roommate_preference = models.CharField(max_length=200, blank=True)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.semester}"

class CounselingAppointment(models.Model):
    SESSION_TYPE = [
        ('IN_PERSON', 'In-person'),
        ('VIRTUAL', 'Virtual'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counseling_appointments')
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counselor_appointments')
    date = models.DateField()
    time = models.TimeField()
    session_type = models.CharField(max_length=10, choices=SESSION_TYPE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='SCHEDULED')
    
    def __str__(self):
        return f"{self.student.username} - {self.date}"

class HealthRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_type = models.CharField(max_length=100)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.visit_date}"

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    capacity = models.IntegerField()
    enrolled = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class ComplianceReport(models.Model):
    REPORT_STATUS = [
        ('DRAFT', 'Draft'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=100)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    generated_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=12, choices=REPORT_STATUS)
    file_path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class Audit(models.Model):
    AUDIT_STATUS = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    audit_type = models.CharField(max_length=100)
    start_date = models.DateField()
    due_date = models.DateField()
    assigned_to = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=AUDIT_STATUS)
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.audit_type} - {self.start_date}"
