# Generated by Django 4.0.4 on 2022-08-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("audit", "0008_alter_access_options_rename_user_id_access_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="access",
            name="role",
            field=models.CharField(
                choices=[
                    ("auditee_contact", "Auditee Contact"),
                    ("auditee_cert", "Auditee Certifying Official"),
                    ("auditor_contact", "Auditor Contact"),
                    ("auditor_cert", "Auditor Certifying Official"),
                    ("creator", "Audit Creator"),
                ],
                help_text="Access type granted to this user",
                max_length=15,
            ),
        ),
        migrations.AddConstraint(
            model_name="access",
            constraint=models.UniqueConstraint(
                condition=models.Q(("role", "creator")),
                fields=("sac",),
                name="audit_$(class)s_single_creator",
            ),
        ),
        migrations.AddConstraint(
            model_name="access",
            constraint=models.UniqueConstraint(
                condition=models.Q(("role", "auditee_cert")),
                fields=("sac",),
                name="audit_$(class)s_single_certifying_auditee",
            ),
        ),
        migrations.AddConstraint(
            model_name="access",
            constraint=models.UniqueConstraint(
                condition=models.Q(("role", "auditor_cert")),
                fields=("sac",),
                name="audit_access_single_certifying_auditor",
            ),
        ),
    ]