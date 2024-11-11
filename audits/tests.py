import pytest
from django.urls import reverse
from rest_framework.test import APITestCase
from audits.models import DESTROY, CREATE, AuditLog
from snippets.factories import UserFactory
from snippets.models import Snippet
from django.contrib.auth.models import User


class BaseAPITest(APITestCase):
    def setUp(self):
        # Set up the API client for the test class
        self.user = UserFactory(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)  # type: ignore


@pytest.mark.django_db
class TestAuditLogger(BaseAPITest):
    def test__log__api_delete_user(self):
        user = UserFactory.create()
        self.client.delete(reverse("user-detail", args=[user.id]))
        audit_logs = AuditLog.objects.all()
        assert len(audit_logs) == 1
        audit_log = audit_logs[0]
        assert audit_log.model_id == user.id
        assert audit_log.model_name == "User"
        assert audit_log.action == DESTROY

    def test__log__api_create_snippet(self):
        data = {
            "title": "Dork",
            "code": "some code",
            "linenos": 0,
            "owner_id": self.user.id,
        }
        self.client.post(reverse("snippet-list"), data, format="json")
        snippet = Snippet.objects.first()
        audit_logs = AuditLog.objects.all()
        assert len(audit_logs) == 1
        audit_log = audit_logs[0]
        assert audit_log.model_id == snippet.id
        assert audit_log.model_name == "Snippet"
        assert audit_log.action == CREATE

    def test__log__api_create_user(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password": "pass",
            "last_name": "last name",
            "first_name": "first name",
        }
        result = self.client.post(reverse("user-list"), data, format="json")
        created_user = User.objects.get(pk=result.data["id"])
        audit_logs = AuditLog.objects.all()
        assert len(audit_logs) == 1
        audit_log = audit_logs[0]
        assert audit_log.model_id == created_user.id
        assert audit_log.model_name == "User"
        assert audit_log.action == CREATE
