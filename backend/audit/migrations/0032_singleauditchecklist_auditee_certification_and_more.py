# Generated by Django 4.2.3 on 2023-08-07 18:21

import audit.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0031_singleauditreportfile_component_page_numbers"),
    ]

    operations = [
        migrations.AddField(
            model_name="singleauditchecklist",
            name="auditee_certification",
            field=models.JSONField(
                blank=True,
                null=True,
                validators=[audit.validators.validate_auditee_certification_json],
            ),
        ),
        migrations.AddField(
            model_name="singleauditchecklist",
            name="auditor_certification",
            field=models.JSONField(
                blank=True,
                null=True,
                validators=[audit.validators.validate_auditor_certification_json],
            ),
        ),
    ]
