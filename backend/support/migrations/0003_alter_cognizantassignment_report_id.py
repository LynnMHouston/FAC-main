# Generated by Django 4.2.5 on 2023-10-02 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("support", "0002_cognizantbaseline_source_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cognizantassignment",
            name="report_id",
            field=models.CharField(),
        ),
    ]