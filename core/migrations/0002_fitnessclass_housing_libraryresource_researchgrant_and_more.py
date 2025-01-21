# Generated by Django 5.1.5 on 2025-01-21 17:48

import core.models
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FitnessClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("instructor", models.CharField(max_length=100)),
                ("schedule", models.CharField(max_length=100)),
                ("capacity", models.IntegerField()),
                ("enrolled", models.IntegerField(default=0)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Housing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("building", models.CharField(max_length=100)),
                ("room_number", models.CharField(max_length=10)),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("SINGLE", "Single"),
                            ("DOUBLE", "Double"),
                            ("SUITE", "Suite"),
                        ],
                        max_length=10,
                    ),
                ),
                ("capacity", models.IntegerField()),
                ("occupied", models.IntegerField(default=0)),
                ("semester_fee", models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name="LibraryResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                (
                    "resource_type",
                    models.CharField(
                        choices=[
                            ("BOOK", "Book"),
                            ("EBOOK", "E-Book"),
                            ("JOURNAL", "Journal"),
                            ("ARTICLE", "Article"),
                            ("MULTIMEDIA", "Multimedia"),
                        ],
                        max_length=10,
                    ),
                ),
                ("isbn", models.CharField(blank=True, max_length=13)),
                ("location", models.CharField(max_length=100)),
                ("available_copies", models.IntegerField(default=1)),
                ("total_copies", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="ResearchGrant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("deadline", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("CLOSED", "Closed"),
                            ("UNDER_REVIEW", "Under Review"),
                            ("AWARDED", "Awarded"),
                        ],
                        max_length=12,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="academicyear",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="academicyear",
            name="name",
        ),
        migrations.RemoveField(
            model_name="academicyear",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="department",
            name="description",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="number",
        ),
        migrations.RemoveField(
            model_name="semester",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="academicyear",
            name="year",
            field=models.CharField(default="2024-2025", max_length=9),
        ),
        migrations.AlterField(
            model_name="academicyear",
            name="end_date",
            field=models.DateField(default=core.models.get_default_end_date),
        ),
        migrations.AlterField(
            model_name="academicyear",
            name="start_date",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name="department",
            name="head",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="department_head",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="semester",
            name="name",
            field=models.CharField(
                choices=[("FALL", "Fall"), ("SPRING", "Spring"), ("SUMMER", "Summer")],
                max_length=6,
            ),
        ),
        migrations.CreateModel(
            name="Audit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("audit_type", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("due_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PLANNED", "Planned"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                        ],
                        max_length=12,
                    ),
                ),
                ("findings", models.TextField(blank=True)),
                ("recommendations", models.TextField(blank=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplianceReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("report_type", models.CharField(max_length=100)),
                ("generated_on", models.DateTimeField(auto_now_add=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("UNDER_REVIEW", "Under Review"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                        ],
                        max_length=12,
                    ),
                ),
                ("file_path", models.CharField(max_length=255)),
                (
                    "generated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CounselingAppointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                (
                    "session_type",
                    models.CharField(
                        choices=[("IN_PERSON", "In-person"), ("VIRTUAL", "Virtual")],
                        max_length=10,
                    ),
                ),
                ("reason", models.TextField()),
                ("status", models.CharField(default="SCHEDULED", max_length=20)),
                (
                    "counselor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="counselor_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="counseling_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=10, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("credits", models.IntegerField()),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.department",
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("prerequisites", models.ManyToManyField(blank=True, to="core.course")),
            ],
        ),
        migrations.CreateModel(
            name="FacultyProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=100)),
                ("office_location", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                ("bio", models.TextField(blank=True)),
                ("joining_date", models.DateField()),
                (
                    "department",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.department",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HealthRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("visit_date", models.DateField()),
                ("visit_type", models.CharField(max_length=100)),
                ("diagnosis", models.TextField(blank=True)),
                ("prescription", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HousingApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("preferred_building", models.CharField(max_length=100)),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("SINGLE", "Single"),
                            ("DOUBLE", "Double"),
                            ("SUITE", "Suite"),
                        ],
                        max_length=10,
                    ),
                ),
                ("roommate_preference", models.CharField(blank=True, max_length=200)),
                ("special_requests", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.semester"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LibraryBorrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateField()),
                ("due_date", models.DateField()),
                ("return_date", models.DateField(blank=True, null=True)),
                ("renewals", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.libraryresource",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Publication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=300)),
                ("journal", models.CharField(max_length=200)),
                ("publication_date", models.DateField()),
                ("doi", models.CharField(blank=True, max_length=100)),
                ("citation_count", models.IntegerField(default=0)),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.facultyprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResearchProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("budget", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PLANNING", "Planning"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                            ("ON_HOLD", "On Hold"),
                        ],
                        max_length=12,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "co_investigators",
                    models.ManyToManyField(
                        related_name="co_investigator_projects",
                        to="core.facultyprofile",
                    ),
                ),
                (
                    "principal_investigator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.facultyprofile",
                    ),
                ),
            ],
        ),
    ]
