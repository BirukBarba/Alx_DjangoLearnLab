from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

"""
Serializers for Author and Book Models
--------------------------------------

BookSerializer:
    - Serializes all fields of the Book model.
    - Contains custom validation ensuring publication_year is not in the future.

AuthorSerializer:
    - Serializes the author's name.
    - Includes a nested list of BookSerializer results using the reverse
      relationship (author.books).
    - Demonstrates how nested objects can be serialized using DRF.

Relationship Handling:
    - The AuthorSerializer uses the related_name='books' defined in the Book model.
    - This allows us to easily include BookSerializer(data=author.books.all(), many=True).
"""


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  
    # The nested serializer uses reverse relationship `author.books`

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
