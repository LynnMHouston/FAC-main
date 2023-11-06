# Generated by Django 4.2.5 on 2023-10-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audit", "0003_alter_singleauditchecklist_data_source_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="cognizant_agency",
            field=models.CharField(
                blank=True,
                help_text="Agency assigned to this large submission. Computed when the submisson is finalized, but may be overridden",
                max_length=2,
                null=True,
                verbose_name="Cog Agency",
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="oversight_agency",
            field=models.CharField(
                blank=True,
                help_text="Agency assigned to this not so large submission. Computed when the submisson is finalized",
                max_length=2,
                null=True,
                verbose_name="OSight Agency",
            ),
        ),
    ]