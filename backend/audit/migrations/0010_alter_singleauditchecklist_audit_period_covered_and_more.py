# Generated by Django 4.0.4 on 2022-08-12 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0009_alter_access_role_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="audit_period_covered",
            field=models.CharField(
                blank=True,
                choices=[
                    ("annual", "Annual"),
                    ("biennial", "Biennial"),
                    ("other", "Other"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="audit_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("single-audit", "Single Audit"),
                    ("program-specific", "Program-Specific Audit"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_address_line_1",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_contact_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_contact_title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_email",
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_phone",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_state",
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditee_zip",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_address_line_1",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_contact_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_contact_title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_ein",
            field=models.CharField(
                blank=True, max_length=12, null=True, verbose_name="Auditor EIN"
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_ein_not_an_ssn_attestation",
            field=models.BooleanField(
                blank=True,
                null=True,
                verbose_name="Attestation: Auditor EIN Not an SSN",
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_email",
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_firm_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_phone",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="auditor_zip",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="ein",
            field=models.CharField(
                blank=True,
                help_text="Auditee Employer Identification Number",
                max_length=12,
                null=True,
                verbose_name="EIN",
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="ein_not_an_ssn_attestation",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Attestation: EIN Not an SSN"
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="multiple_eins_covered",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Multiple EINs covered"
            ),
        ),
        migrations.AlterField(
            model_name="singleauditchecklist",
            name="multiple_ueis_covered",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Multiple UEIs covered"
            ),
        ),
    ]