# Generated by Django 4.2.3 on 2023-09-14 09:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("support", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CognizantAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("report_id", models.CharField(max_length=17)),
                (
                    "cognizant_agency",
                    models.CharField(max_length=2, verbose_name="Cog Agency"),
                ),
                (
                    "date_assigned",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date Assigned"
                    ),
                ),
                (
                    "assignor_email",
                    models.EmailField(max_length=254, verbose_name="Email"),
                ),
                ("override_comment", models.TextField(verbose_name="Comment")),
                (
                    "assignment_type",
                    models.CharField(
                        choices=[
                            ("computed", "Computed by FAC"),
                            ("manual", "Manual Override"),
                        ],
                        default="computed",
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cognizantbaseline",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
        migrations.AlterField(
            model_name="cognizantbaseline",
            name="cognizant_agency",
            field=models.CharField(max_length=2, verbose_name="Cog Agency"),
        ),
        migrations.AlterField(
            model_name="cognizantbaseline",
            name="date_assigned",
            field=models.DateTimeField(null=True, verbose_name="Date Assigned"),
        ),
        migrations.AlterField(
            model_name="cognizantbaseline",
            name="dbkey",
            field=models.CharField(max_length=20, null=True, verbose_name="dbkey"),
        ),
        migrations.AlterField(
            model_name="cognizantbaseline",
            name="ein",
            field=models.CharField(max_length=30, null=True, verbose_name="EIN"),
        ),
        migrations.AlterField(
            model_name="cognizantbaseline",
            name="uei",
            field=models.CharField(max_length=30, null=True, verbose_name="UEI"),
        ),
    ]