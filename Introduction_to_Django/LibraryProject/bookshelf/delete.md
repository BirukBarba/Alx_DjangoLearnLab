# Delete Operation

# Open the Django shell:
# python manage.py shell

from bookshelf.models import Book

# Retrieve the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Confirm deletion by retrieving all books
print(Book.objects.all())

# Expected Output:
# Output:
# <QuerySet []>