# Generated by Django 5.2.4 on 2025-07-19 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "course_material",
            "0004_alter_batch_options_alter_classresource_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="batch",
            options={
                "ordering": ["start_date"],
                "verbose_name": "3. Batch",
                "verbose_name_plural": "3. Batches",
            },
        ),
        migrations.AlterModelOptions(
            name="classresource",
            options={
                "ordering": ["class_date", "created_at"],
                "verbose_name": "5. Class Resource",
                "verbose_name_plural": "5. Class Resources",
            },
        ),
        migrations.AlterModelOptions(
            name="course",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "2. Course",
                "verbose_name_plural": "2. Courses",
            },
        ),
        migrations.AlterModelOptions(
            name="exam",
            options={
                "ordering": ["start_datetime"],
                "verbose_name": "6. Exam",
                "verbose_name_plural": "6. Exams",
            },
        ),
        migrations.AlterModelOptions(
            name="instructor",
            options={
                "verbose_name": "1. Instructor",
                "verbose_name_plural": "1. Instructors",
            },
        ),
        migrations.AlterModelOptions(
            name="recording",
            options={
                "ordering": ["-class_date", "-created_at"],
                "verbose_name": "4. Recording",
                "verbose_name_plural": "4. Recordings",
            },
        ),
    ]
