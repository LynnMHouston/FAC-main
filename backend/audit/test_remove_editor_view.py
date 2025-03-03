from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from .models import (
    Access,
    DeletedAccess,
    SingleAuditChecklist,
    User,
)


class RemoveEditorViewTests(TestCase):
    """
    GET and POST tests for removing editors from a submission.
    """

    role = "editor"
    view = "audit:RemoveEditorView"

    def test_basic_get(self):
        """
        An editor should be able to access this page for a SAC they're associated
        with, but they can't remove their own access.
        """
        user = baker.make(User, email="editor@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        access = baker.make(Access, user=user, email=user.email, sac=sac, role="editor")
        sac.save()

        url = (
            f"{reverse(self.view, kwargs={'report_id': sac.report_id})}?id={access.id}"
        )
        response = self.client.get(url)

        self.assertIn(
            "You do not have permission to remove audit access for this editor",
            response.content.decode("utf-8"),
        )

    def test_id_404(self):
        """
        Should 404 when an editor tries to reach or remove access for an editor
        that doesn't exist.
        """
        user = baker.make(User, email="editor@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        baker.make(Access, user=user, email=user.email, sac=sac, role="editor")
        sac.save()

        url = f"{reverse(self.view, kwargs={'report_id': sac.report_id})}?id=999999999"  # Fake id

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 404)

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 404)

    def test_role_404(self):
        """
        Should 404 when an editor tries to reach or remove access for someone
        that isn't an editor.
        """
        user = baker.make(User, email="editor@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        baker.make(Access, user=user, email=user.email, sac=sac, role="editor")
        access_to_remove = baker.make(
            Access,
            sac=sac,
            role="foobar",  # Non-editor role
        )
        sac.save()

        url = f"{reverse(self.view, kwargs={'report_id': sac.report_id})}?id={access_to_remove.id}"

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 404)

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 404)

    def test_403(self):
        """
        Should 403 when a non-editor tries to reach or remove an Access.
        """
        user = baker.make(User, email="editor@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        baker.make(
            Access, user=user, email=user.email, sac=sac, role="foobar"
        )  # Non-editor role
        access_to_remove = baker.make(
            Access,
            sac=sac,
            role="editor",
        )
        sac.save()

        url = f"{reverse(self.view, kwargs={'report_id': sac.report_id})}?id={access_to_remove.id}"

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 403)

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 403)

    def test_invalid_post(self):
        """
        Submitting the form for yourself should error.
        """
        user = baker.make(User, email="editor@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        access = baker.make(Access, user=user, email=user.email, sac=sac, role="editor")
        sac.save()

        data = {
            "editor_id": access.id,
        }
        url = reverse(self.view, kwargs={"report_id": sac.report_id})
        response = self.client.post(url, data=data)

        self.assertIn(
            "You do not have permission to remove audit access for this editor",
            response.content.decode("utf-8"),
        )

    def test_basic_post(self):
        """
        Submitting the form should delete the existing Access and create a DeletedAccess.
        """
        user = baker.make(User, email="removing_user@example.com")
        self.client.force_login(user)

        sac = baker.make(SingleAuditChecklist)
        sac.general_information = {"auditee_uei": "YESIAMAREALUEI"}
        baker.make(Access, user=user, email=user.email, sac=sac, role="editor")
        access_to_remove = baker.make(
            Access,
            sac=sac,
            role="editor",
            email="contact@example.com",
        )
        sac.save()

        data = {
            "editor_id": access_to_remove.id,
        }
        url = reverse(self.view, kwargs={"report_id": sac.report_id})
        response = self.client.post(url, data=data)

        self.assertEqual(302, response.status_code)

        deleted_access = DeletedAccess.objects.get(
            sac=sac,
            fullname=access_to_remove.fullname,
            email=access_to_remove.email,
        )
        self.assertEqual(self.role, deleted_access.role)
