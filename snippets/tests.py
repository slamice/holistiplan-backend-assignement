from django.test import TestCase
from rest_framework.test import APIClient
from snippets.factories import SnippetFactory, UserFactory
from snippets.models import Snippet
import pytest
from snippets.views import SnippetList


@pytest.mark.django_db
class TestSnippetList:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        # Set up the API client for the test class
        self.api_client = APIClient()

    def test__get_queryset__no_objects(self):
        """Test that the view returns no snippets."""
        response = self.api_client.get("/snippets/")
        breakpoint()
        assert response.data["results"] == []

    def test__get_queryset(self):
        """Test that the view returns no snippets."""
        user = UserFactory.create()
        SnippetFactory.create(owner=user)
        response = self.api_client.get("/snippets/")
        breakpoint()
        assert len(response.data["results"]) == 1
