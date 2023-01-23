# Generated by Django 4.1.4 on 2023-01-23 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_distro", "0033_alter_general_cpa_street2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="general",
            name="sp_framework",
            field=models.CharField(
                max_length=40,
                null=True,
                verbose_name="Special Purpose Framework that was used as the basis of accounting",
            ),
        ),
    ]
