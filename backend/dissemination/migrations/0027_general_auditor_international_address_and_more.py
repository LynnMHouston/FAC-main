# Generated by Django 4.2.3 on 2023-08-25 07:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dissemination", "0026_additionaluei_alter_captext_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="general",
            name="auditor_international_address",
            field=models.TextField(
                help_text="Data sources: SF-SAC 2019-2021: I/6/c; SF-SAC 2022: I/6/c Census mapping: GENERAL, CPACOUNTRY",
                null=True,
                verbose_name="CPA non-USA address",
            ),
        ),
        migrations.AlterField(
            model_name="general",
            name="auditor_country",
            field=models.TextField(
                help_text="Data sources: SF-SAC 2019-2021: I/6/c; SF-SAC 2022: I/6/c Census mapping: GENERAL, CPACOUNTRY",
                null=True,
                verbose_name="CPA Country - USA or non-USA",
            ),
        ),
    ]
