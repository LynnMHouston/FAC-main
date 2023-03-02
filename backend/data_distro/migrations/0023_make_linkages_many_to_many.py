# Generated by Django 4.1.4 on 2023-02-26 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_distro", "0022_rename_models"),
    ]

    operations = [
        # EINs were not pointing to audiotapes, they were pointing to cpa_ein in federal awards
        migrations.RemoveField(
            model_name="auditee",
            name="agency",
        ),
        # needs to accommodate many notes
        migrations.RemoveField(
            model_name="general",
            name="note",
        ),
        migrations.AddField(
            model_name="general",
            name="notes",
            field=models.ManyToManyField(to="data_distro.note"),
        ),
        # needs many to many
        migrations.RemoveField(
            model_name="general",
            name="cap_text",
        ),
        # many to many because there are more lines in the cfda table than the gen table
        migrations.RemoveField(
            model_name="general",
            name="federal_awards",
        ),
        migrations.RemoveField(
            model_name="general",
            name="passthrough",
        ),
        migrations.AddField(
            model_name="general",
            name="cap_text",
            field=models.ManyToManyField(to="data_distro.captext"),
        ),
        migrations.AddField(
            model_name="general",
            name="federal_awards",
            field=models.ManyToManyField(to="data_distro.federalaward"),
        ),
        migrations.AddField(
            model_name="general",
            name="passthrough",
            field=models.ManyToManyField(to="data_distro.passthrough"),
        ),
    ]