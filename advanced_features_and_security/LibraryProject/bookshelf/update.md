from bookshelf.models import Book

# Retrieve the existing book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
book.title