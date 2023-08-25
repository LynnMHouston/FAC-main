# Generated by Django 4.2.3 on 2023-08-24 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("audit", "0037_access_fullname"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmissionEvent",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.CharField(
                        choices=[
                            ("additional-eins-updated", "Additional EINs updated"),
                            ("additional-ueis-updated", "Additional UEIs updated"),
                            ("audit-information-updated", "Audit information updated"),
                            ("audit-report-pdf-updated", "Audit report PDF updated"),
                            (
                                "auditee-certification-completed",
                                "Auditee certification completed",
                            ),
                            (
                                "auditor-certification-completed",
                                "Auditor certification completed",
                            ),
                            (
                                "corrective-action-plan-updated",
                                "Corrective action plan updated",
                            ),
                            ("created", "Created"),
                            ("federal-awards-updated", "Federal awards updated"),
                            (
                                "federal-awards-audit-findings-updated",
                                "Federal awards audit findings updated",
                            ),
                            (
                                "federal-awards-audit-findings-text-updated",
                                "Federal awards audit findings text updated",
                            ),
                            (
                                "findings-uniform-guidance-updated",
                                "Findings uniform guidance updated",
                            ),
                            (
                                "general-information-updated",
                                "General information updated",
                            ),
                            ("locked-for-certification", "Locked for certification"),
                            ("notes-to-sefa-updated", "Notes to SEFA updated"),
                            (
                                "secondary-auditors-updated",
                                "Secondary auditors updated",
                            ),
                            ("submitted", "Submitted to the FAC for processing"),
                        ]
                    ),
                ),
                (
                    "sac",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="audit.singleauditchecklist",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
