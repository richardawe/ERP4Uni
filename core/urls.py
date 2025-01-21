from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'academic-years', views.AcademicYearViewSet)
router.register(r'semesters', views.SemesterViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'faculty-profiles', views.FacultyProfileViewSet)
router.register(r'publications', views.PublicationViewSet)
router.register(r'research-grants', views.ResearchGrantViewSet)
router.register(r'research-projects', views.ResearchProjectViewSet)
router.register(r'library-resources', views.LibraryResourceViewSet)
router.register(r'library-borrowings', views.LibraryBorrowingViewSet)
router.register(r'housing', views.HousingViewSet)
router.register(r'housing-applications', views.HousingApplicationViewSet)
router.register(r'counseling-appointments', views.CounselingAppointmentViewSet)
router.register(r'health-records', views.HealthRecordViewSet)
router.register(r'fitness-classes', views.FitnessClassViewSet)
router.register(r'compliance-reports', views.ComplianceReportViewSet)
router.register(r'audits', views.AuditViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login, name='api-login'),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
    path('recent-activities/', views.recent_activities, name='recent-activities'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] 