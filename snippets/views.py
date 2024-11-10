from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q

from .models import Snippet, soft_delete_user
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer

import logging

logger = logging.getLogger(__name__)


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetList(generics.ListCreateAPIView):
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        result = None
        try:
            result = Snippet.objects.all()
        except Exception as e:
            logging.warning(f"Could not find Snippet objects: {e}")

        return result

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        result = None
        try:
            result = Snippet.objects.first()
        except Exception as e:
            logging.warning(f"Could not find Snippet objects: {e}")

        return result


class UserCreateList(
    generics.ListCreateAPIView,
):
    serializer_class = UserSerializer
    """
    List or create products.

    Query Parameters:
    - `include_soft_deletes` (str): Tells an admin if they can include soft delete.
    """

    def get_queryset(self):
        include_soft_deletes = self.request.query_params.get(
            "include_soft_deletes", "False"
        )
        query = User.objects

        if self.request.user.is_staff and include_soft_deletes == "True":
            return query.all()

        return query.filter(
            Q(soft_delete_status__isnull=True) | Q(soft_delete_status=False)
        )

    def get_permissions(self):
        method = self.request.method
        if method == "POST":
            return [permissions.IsAdminUser()]  # Only authenticated users can create
        return [permissions.IsAuthenticatedOrReadOnly()]  # Anyone can view


class UserDetail(
    generics.RetrieveAPIView,
    generics.DestroyAPIView,
):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(
            Q(soft_delete_status__isnull=True) | Q(soft_delete_status=False)
        )

    def get_permissions(self):
        method = self.request.method
        if method == "DELETE":
            return [permissions.IsAdminUser()]  # Only authenticated users can create
        return [permissions.IsAuthenticatedOrReadOnly()]  # Anyone can view

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        soft_delete_user(user)
        return Response(
            {"detail": "User soft-deleted."}, status=status.HTTP_204_NO_CONTENT
        )
