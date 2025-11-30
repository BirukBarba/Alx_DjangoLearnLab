from django.db import models

# Create your models here.
from django.db import models

"""
Author and Book Models
----------------------

Author:
    Represents a book author with a simple name field.

Book:
    Represents a book written by an author, including:
        - title
        - publication year
        - a foreign key linking it to the Author model

Relationship:
    One Author → Many Books (one-to-many)
    Each Book references a single Author.

These models will be used to demonstrate nested serialization.
"""

class Author(models.Model):
    name = models.CharField(max_length=255)  # Stores author name

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)  # Book title
    publication_year = models.IntegerField()   # Year of publication
    author = models.ForeignKey(
        Author,
        related_name='books',  # Makes reverse lookup possible (author.books.all())
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
