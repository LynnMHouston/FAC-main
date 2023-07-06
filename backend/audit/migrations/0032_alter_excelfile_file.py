# Generated by Django 4.2.1 on 2023-07-05 21:48

import audit.models
import audit.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0031_alter_singleauditchecklist_transition_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="excelfile",
            name="file",
            field=models.FileField(
                upload_to=audit.models.excel_file_path,
                validators=[audit.validators.validate_excel_file],
            ),
        ),
    ]