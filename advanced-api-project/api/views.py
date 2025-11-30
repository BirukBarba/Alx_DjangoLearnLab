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



from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer

"""
Enhanced BookListView with Advanced Querying
--------------------------------------------

This view now supports:

1. Filtering:
   - Filter by title, publication_year, and author using:
     /api/books/?title=Name
     /api/books/?publication_year=2020
     /api/books/?author=1

2. Searching:
   - Search across title and author name using:
     /api/books/?search=tolkien

3. Ordering:
   - Order by title, publication_year, or any model field:
     /api/books/?ordering=title
     /api/books/?ordering=-publication_year

These capabilities provide a rich query interface for API consumers.
"""

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Filtering fields
    filterset_fields = ['title', 'publication_year', 'author']

    # Enable search across fields
    search_fields = ['title', 'author__name']

    # Allow ordering by fields
    ordering_fields = ['title', 'publication_year', 'id']

    # Optional: default ordering
    ordering = ['title']
