from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Author, Book


"""
API View Tests for Book Endpoints
---------------------------------

This test suite covers:
    - CRUD operations
    - Permissions
    - Filtering
    - Searching
    - Ordering

All tests use Django's built-in test runner and DRF's APIClient.
A separate test database ensures that these tests do not affect
development or production databases.
"""


class BookAPITestCase(APITestCase):
    """Test suite for Book API endpoints."""

    def setUp(self):
        """
        Prepare test data and test client.

        - Create test user for authenticated actions.
        - Create sample authors and books.
        """
        self.client = APIClient()

        # Create user for authenticated actions
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Test authors
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")

        # Test books
        self.book1 = Book.objects.create(
            title="The Hobbit", publication_year=1937, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Lord of the Rings", publication_year=1954, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984", publication_year=1949, author=self.author2
        )

    # ----------------------------------------------------------------------
    # LIST VIEW TESTS
    # ----------------------------------------------------------------------

    def test_list_books(self):
        """Test retrieving the list of books."""
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        url = reverse("book-list") + f"?author={self.author1.id}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    def test_search_books(self):
        """Test searching books using search filter."""
        url = reverse("book-list") + "?search=Hobbit"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The Hobbit")

    def test_order_books(self):
        """Test ordering books by publication_year."""
        url = reverse("book-list") + "?ordering=-publication_year"
        response = self.client.get(url)

        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ----------------------------------------------------------------------
    # DETAIL VIEW TESTS
    # ----------------------------------------------------------------------

    def test_get_single_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(reverse("book-detail", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Hobbit")

    # ----------------------------------------------------------------------
    # CREATE VIEW TESTS
    # ----------------------------------------------------------------------

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create a book."""
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(reverse("book-create"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users can create a new book."""
        self.client.login(username="testuser", password="password123")

        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(reverse("book-create"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    # ----------------------------------------------------------------------
    # UPDATE VIEW TESTS
    # ----------------------------------------------------------------------

    def test_update_book_unauthenticated(self):
        """Unauthenticated users cannot update a book."""
        data = {"title": "Unauthorized Update"}
        response = self.client.patch(
            reverse("book-update", args=[self.book1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Authenticated users can update a book."""
        self.client.login(username="testuser", password="password123")

        data = {"title": "The Hobbit — Updated"}
        response = self.client.patch(
            reverse("book-update", args=[self.book1.id]),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh object
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Hobbit — Updated")

    # ----------------------------------------------------------------------
    # DELETE VIEW TESTS
    # ----------------------------------------------------------------------

    def test_delete_book_unauthenticated(self):
        """Unauthenticated users cannot delete a book."""
        response = self.client.delete(reverse("book-delete", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book."""
        self.client.login(username="testuser", password="password123")

        response = self.client.delete(reverse("book-delete", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
