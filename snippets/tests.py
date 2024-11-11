from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from snippets.factories import SnippetFactory, UserFactory
from snippets.models import Snippet, soft_delete_user
import pytest
from django.urls import reverse
import base64
from rest_framework.test import APITestCase

from snippets.views import SnippetList


def get_basic_auth_headers(username, password):
    # Encode the credentials in the format "username:password"
    credentials = f"{username}:{password}".encode("utf-8")
    base64_credentials = base64.b64encode(credentials).decode("utf-8")
    return {"HTTP_AUTHORIZATION": f"Basic {base64_credentials}"}


class BaseAPITest(APITestCase):
    def setUp(self):
        # Set up the API client for the test class
        self.user = UserFactory(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)


@pytest.mark.django_db
class TestSnippetList(BaseAPITest):
    def test__get_queryset__no_objects(self):
        """Test that the view returns no snippets."""
        response = self.client.get(reverse("snippet-list"))
        assert response.data["results"] == []

    def test__get_queryset(self):
        """Test that the view returns no snippets."""
        user = UserFactory.create()
        SnippetFactory.create(owner=user)
        response = self.client.get(reverse("snippet-list"))
        assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestUserDetail(BaseAPITest):
    def undo_staff(self):
        self.user.is_staff = False
        self.user.save()

    def test__delete_user__not_admin(self):
        self.undo_staff()
        response = self.client.delete(reverse("user-detail", args=[0]))
        assert response.status_code == 403  # type: ignore

    def test__delete_user__admin(self):
        user = UserFactory.create()
        response = self.client.delete(reverse("user-detail", args=[user.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
        assert user.soft_delete_status.is_deleted == True

    def test__delete_user__user_doesnt_exist(self):
        response = self.client.delete(reverse("user-detail", args=[0]))
        assert response.status_code == 404  # type: ignore

    def test__list_users__cant_see_deleted_user(self):
        user = UserFactory.create()
        response = self.client.get(reverse("user-list"))
        assert response.data["count"] == 2

        soft_delete_user(user)
        self.undo_staff()

        response = self.client.get(reverse("user-list"))
        assert response.data["count"] == 1

    def test__list_users__admin_can_see_deleted_user(self):
        user = UserFactory.create()
        soft_delete_user(user)
        response = self.client.get(
            reverse("user-list"), data={"include_soft_deletes": "True"}
        )
        assert response.data["count"] == 2
