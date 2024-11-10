import factory
from .models import Snippet
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")  # Faker generates a random username
    email = factory.Faker("email")  # Faker generates a random email
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class SnippetFactory(DjangoModelFactory):
    class Meta:
        model = Snippet
