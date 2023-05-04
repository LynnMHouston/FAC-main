# Generated by Django 4.1.7 on 2023-04-26 14:14

import audit.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0019_singleauditchecklist_corrective_action_plan_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="singleauditchecklist",
            name="findings_text",
            field=models.JSONField(
                blank=True,
                null=True,
                validators=[audit.validators.validate_findings_text_json],
            ),
        ),
    ]