# Generated by Django 4.1.4 on 2023-01-20 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_distro", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DunInfo",
            new_name="DunsInfo",
        ),
        migrations.AddField(
            model_name="general",
            name="date_firewall",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="general",
            name="previous_date_firewall",
            field=models.DateField(null=True),
        ),
    ]
