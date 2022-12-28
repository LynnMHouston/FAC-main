# Generated by Django 4.1.4 on 2022-12-16 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0015_singleauditchecklist_general_information"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="audit_period_covered",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_address_line_1",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_city",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_contact_name",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_contact_title",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_email",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_fiscal_period_end",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_fiscal_period_start",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_name",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_phone",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_state",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_uei",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditee_zip",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_address_line_1",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_city",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_contact_name",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_contact_title",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_country",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_ein",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_ein_not_an_ssn_attestation",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_email",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_firm_name",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_phone",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_state",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="auditor_zip",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="ein",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="ein_not_an_ssn_attestation",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="is_usa_based",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="met_spending_threshold",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="multiple_eins_covered",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="multiple_ueis_covered",
        ),
        migrations.RemoveField(
            model_name="singleauditchecklist",
            name="user_provided_organization_type",
        ),
    ]
