# Generated by Django 4.1.7 on 2023-03-10 21:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_distro", "0027_null_for_auditee_auditee_contact"),
    ]

    operations = [
        migrations.AddField(
            model_name="general",
            name="pdf_urls",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    max_length=400,
                    null=True,
                    verbose_name="PDFs associated with the report",
                ),
                null=True,
                size=None,
            ),
        ),
    ]