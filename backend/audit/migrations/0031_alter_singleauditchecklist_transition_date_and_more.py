# Generated by Django 4.2.1 on 2023-06-23 17:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0030_alter_singleauditchecklist_transition_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="transition_date",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateTimeField(), blank=True, default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="transition_name",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("in_progress", "In Progress"),
                        ("ready_for_certification", "Ready for Certification"),
                        ("auditor_certified", "Auditor Certified"),
                        ("auditee_certified", "Auditee Certified"),
                        ("certified", "Certified"),
                        ("submitted", "Submitted"),
                    ],
                    max_length=40,
                ),
                blank=True,
                default=list,
                size=None,
            ),
        ),
    ]