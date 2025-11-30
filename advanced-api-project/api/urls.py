from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

"""
Book API URL Routing
--------------------

This file contains BOTH:

1. Correct REST endpoints using <pk>
   - /books/<pk>/update/
   - /books/<pk>/delete/

2. The literal endpoints requested by the user:
   - /books/update
   - /books/delete

These non-REST endpoints cannot actually update/delete without a PK,
so they return a clear error message explaining that a book ID is required.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class MissingPKView(APIView):
    """Returns an error when /books/update or /books/delete is accessed without a PK."""
    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "A book ID (pk) is required for this action."},
            status=status.HTTP_400_BAD_REQUEST
        )


urlpatterns = [
    # Standard REST endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),


    path('books/update', MissingPKView.as_view(), name='books-update-no-pk'),
    path('books/delete', MissingPKView.as_view(), name='books-delete-no-pk'),
]
