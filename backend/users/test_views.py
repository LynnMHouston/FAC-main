from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIClient

from .auth import JWTUpsertAuthentication
from .views import AuthToken

from model_bakery import baker

User = get_user_model()

TOKEN_PATH = reverse("token")


class AuthTokenViewTests(TestCase):
    def test_jwt_upsert_auth_required(self):
        view = AuthToken()

        # AuthToken views should require JWTUpsertAuthentication
        self.assertIn(JWTUpsertAuthentication, view.authentication_classes)
        self.assertEqual(len(view.authentication_classes), 1)

        # AuthToken views should require that the user is authenticated
        self.assertIn(IsAuthenticated, view.permission_classes)
        self.assertEqual(len(view.permission_classes), 1)

    def test_no_existing_token(self):
        # if a user has no existing tokens, one should be created
        user = baker.make(User)

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(TOKEN_PATH)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)

    def test_existing_token(self):
        # if a user has an existing token, a new one should be created in its place
        user = baker.make(User)
        token = baker.make(Token, user=user)

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(TOKEN_PATH)

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)
        self.assertNotEqual(token.key, data["token"])