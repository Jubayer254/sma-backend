# Generated by Django 5.2.4 on 2025-07-19 08:09

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Batch",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("monday", models.BooleanField(default=False)),
                ("tuesday", models.BooleanField(default=False)),
                ("wednesday", models.BooleanField(default=False)),
                ("thursday", models.BooleanField(default=False)),
                ("friday", models.BooleanField(default=False)),
                ("saturday", models.BooleanField(default=False)),
                ("sunday", models.BooleanField(default=False)),
                ("class_time", models.TimeField()),
                ("zoom_link", models.URLField(max_length=500)),
                ("zoom_meeting_id", models.CharField(blank=True, max_length=50)),
                ("zoom_passcode", models.CharField(blank=True, max_length=20)),
                ("max_students", models.PositiveIntegerField(default=50)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "batches",
                "ordering": ["start_date"],
            },
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="courses/thumbnails/"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "courses",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ClassResource",
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
                ("description", models.TextField(blank=True)),
                (
                    "class_date",
                    models.DateField(
                        blank=True,
                        help_text="Leave blank for general batch resources",
                        null=True,
                    ),
                ),
                (
                    "resource_type",
                    models.CharField(
                        choices=[
                            ("pdf", "PDF Document"),
                            ("video", "Video"),
                            ("image", "Image"),
                            ("link", "External Link"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
                (
                    "file",
                    models.FileField(blank=True, null=True, upload_to="resources/"),
                ),
                ("external_link", models.URLField(blank=True, max_length=500)),
                ("is_downloadable", models.BooleanField(default=True)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to="course_material.batch",
                    ),
                ),
            ],
            options={
                "db_table": "class_resources",
                "ordering": ["class_date", "uploaded_at"],
            },
        ),
        migrations.AddField(
            model_name="batch",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="batches",
                to="course_material.course",
            ),
        ),
        migrations.CreateModel(
            name="Exam",
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
                ("description", models.TextField(blank=True)),
                ("total_marks", models.PositiveIntegerField(default=100)),
                ("passing_marks", models.PositiveIntegerField(default=50)),
                (
                    "duration",
                    models.DurationField(help_text="Duration in HH:MM:SS format"),
                ),
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("shuffle_questions", models.BooleanField(default=True)),
                ("show_result_immediately", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exams",
                        to="course_material.batch",
                    ),
                ),
            ],
            options={
                "db_table": "exams",
                "ordering": ["start_datetime"],
            },
        ),
        migrations.CreateModel(
            name="Instructor",
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
                ("bio", models.TextField(blank=True)),
                ("expertise", models.CharField(blank=True, max_length=200)),
                (
                    "profile_image",
                    models.ImageField(blank=True, null=True, upload_to="instructors/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "instructors",
            },
        ),
        migrations.AddField(
            model_name="course",
            name="instructors",
            field=models.ManyToManyField(
                related_name="courses", to="course_material.instructor"
            ),
        ),
        migrations.CreateModel(
            name="Question",
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
                ("question_text", models.TextField()),
                ("marks", models.PositiveIntegerField(default=1)),
                ("order", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="course_material.exam",
                    ),
                ),
            ],
            options={
                "db_table": "questions",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Answer",
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
                ("answer_text", models.TextField()),
                ("is_correct", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=1)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="course_material.question",
                    ),
                ),
            ],
            options={
                "db_table": "answers",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Recording",
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
                ("description", models.TextField(blank=True)),
                (
                    "class_date",
                    models.DateField(
                        help_text="Date of the class this recording is for"
                    ),
                ),
                ("recording_url", models.URLField(blank=True, max_length=500)),
                (
                    "recording_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="recordings/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["mp4", "avi", "mov", "wmv"]
                            )
                        ],
                    ),
                ),
                ("duration", models.DurationField(blank=True, null=True)),
                ("is_public", models.BooleanField(default=True)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recordings",
                        to="course_material.batch",
                    ),
                ),
            ],
            options={
                "db_table": "recordings",
                "ordering": ["-class_date", "-uploaded_at"],
            },
        ),
        migrations.CreateModel(
            name="Enrollment",
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
                ("enrollment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("enrolled", "Enrolled"),
                            ("completed", "Completed"),
                            ("dropped", "Dropped"),
                            ("suspended", "Suspended"),
                        ],
                        default="enrolled",
                        max_length=20,
                    ),
                ),
                ("payment_status", models.BooleanField(default=False)),
                ("completion_date", models.DateField(blank=True, null=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrollments",
                        to="course_material.batch",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrollments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "enrollments",
                "ordering": ["-enrollment_date"],
                "unique_together": {("student", "batch")},
            },
        ),
    ]
