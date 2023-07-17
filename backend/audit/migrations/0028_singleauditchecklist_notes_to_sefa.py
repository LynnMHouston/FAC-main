# Generated by Django 4.2.1 on 2023-07-13 16:33

import audit.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0027_singleauditchecklist_additional_ueis_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="singleauditchecklist",
            name="notes_to_sefa",
            field=models.JSONField(
                blank=True,
                null=True,
                validators=[audit.validators.validate_notes_to_sefa_json],
            ),
        ),
    ]
