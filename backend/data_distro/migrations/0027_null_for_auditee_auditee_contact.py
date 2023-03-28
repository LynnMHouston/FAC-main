# Generated by Django 4.1.4 on 2023-03-08 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_distro", "0026_nulls_for_cpa_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auditee",
            name="auditee_contact",
            field=models.CharField(
                help_text="Data sources: SF-SAC 1997-2000: I/6/c; SF-SAC 2001-2003: I/6/c; SF-SAC 2004-2007: I/6/c; SF-SAC 2008-2009: I/5/c; SF-SAC 2010-2012: I/5/c; SF-SAC 2013-2015: I/5/c; SF-SAC 2016-2018: I/5/c; SF-SAC 2019-2021: I/5/c; SF-SAC 2022: I/5/c Census mapping: GENERAL, AUDITEECONTACT",
                max_length=50,
                null=True,
                verbose_name="Name of Auditee Contact",
            ),
        ),
    ]