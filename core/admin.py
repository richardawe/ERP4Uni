from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Department, AcademicYear, Semester, Course, FacultyProfile,
    Publication, ResearchGrant, ResearchProject, LibraryResource,
    LibraryBorrowing, Housing, HousingApplication, CounselingAppointment,
    HealthRecord, FitnessClass, ComplianceReport, Audit
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'department', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'department', 'phone_number')}),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'head')
    search_fields = ('code', 'name')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'academic_year')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credits', 'instructor')
    list_filter = ('department', 'credits')
    search_fields = ('code', 'name')
    filter_horizontal = ('prerequisites',)

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'joining_date')
    list_filter = ('department', 'position')
    search_fields = ('user__username', 'user__email')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'journal', 'publication_date', 'citation_count')
    list_filter = ('journal', 'publication_date')
    search_fields = ('title', 'faculty__user__username')

@admin.register(ResearchGrant)
class ResearchGrantAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'deadline', 'status')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'principal_investigator', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'principal_investigator__user__username')
    filter_horizontal = ('co_investigators',)

@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'resource_type', 'available_copies', 'total_copies')
    list_filter = ('resource_type',)
    search_fields = ('title', 'author', 'isbn')

@admin.register(LibraryBorrowing)
class LibraryBorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'borrow_date', 'due_date', 'return_date')
    list_filter = ('borrow_date', 'due_date')
    search_fields = ('user__username', 'resource__title')

@admin.register(Housing)
class HousingAdmin(admin.ModelAdmin):
    list_display = ('building', 'room_number', 'room_type', 'capacity', 'occupied')
    list_filter = ('room_type', 'building')
    search_fields = ('building', 'room_number')

@admin.register(HousingApplication)
class HousingApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'preferred_building', 'room_type', 'semester', 'status')
    list_filter = ('status', 'room_type', 'semester')
    search_fields = ('student__username', 'preferred_building')

@admin.register(CounselingAppointment)
class CounselingAppointmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'counselor', 'date', 'time', 'session_type', 'status')
    list_filter = ('session_type', 'status', 'date')
    search_fields = ('student__username', 'counselor__username')

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'visit_date', 'visit_type')
    list_filter = ('visit_type', 'visit_date')
    search_fields = ('student__username', 'diagnosis')

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'schedule', 'capacity', 'enrolled')
    list_filter = ('instructor',)
    search_fields = ('name', 'instructor')

@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'generated_on', 'status')
    list_filter = ('report_type', 'status')
    search_fields = ('title', 'generated_by__username')

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('audit_type', 'assigned_to', 'start_date', 'due_date', 'status')
    list_filter = ('status', 'audit_type')
    search_fields = ('audit_type', 'assigned_to__name')
