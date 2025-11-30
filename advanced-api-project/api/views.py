from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

"""
Book API Views using DRF Generic Views
--------------------------------------

This file defines a set of CRUD views for the Book model using DRF’s
powerful generic class-based views.

Views implemented:
    - BookListView:   GET /books/        (list all books)
    - BookDetailView: GET /books/<pk>/   (retrieve single book)
    - BookCreateView: POST /books/       (create new book)
    - BookUpdateView: PUT/PATCH /books/<pk>/ (update existing book)
    - BookDeleteView: DELETE /books/<pk>/    (delete existing book)

Permissions:
    - List + Detail: Read-only access for anonymous users.
    - Create, Update, Delete: Restricted to authenticated users only.

Custom Behavior:
    - Create and Update views rely on serializer validation
      (including custom publication_year validation).
    - Permissions are applied per view using DRF permission classes.
"""

# ---------------------------
# LIST + DETAIL VIEWS
# ---------------------------

class BookListView(generics.ListAPIView):
    """
    ListView:
        Retrieves and returns all Book records.
        Accessible to anyone (read-only for unauthenticated users).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView:
        Retrieves a single Book by its primary key.
        Read-only access for anonymous users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ---------------------------
# CREATE + UPDATE + DELETE VIEWS
# ---------------------------

class BookCreateView(generics.CreateAPIView):
    """
    CreateView:
        Allows authenticated users to add a new Book.
        Uses BookSerializer, which includes custom validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restriction applied here

    def perform_create(self, serializer):
        # Additional custom logic can be added here if needed
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView:
        Allows authenticated users to update an existing Book.
        Includes full validation of fields from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Custom behavior or audit logging could go here
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView:
        Allows authenticated users to delete a Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
