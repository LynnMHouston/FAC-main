# Generated by Django 4.2.1 on 2023-07-19 22:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "dissemination",
            "0008_rename_charts_tables_findingtext_contains_chart_or_table",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="general",
            name="pdf_url",
        ),
    ]