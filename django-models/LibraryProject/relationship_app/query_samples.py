import os
import django

# --- Setup Django environment manually so we can use ORM in this standalone script ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models_project.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Queries ---

def query_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'.")


def list_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name} library:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'.")


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Access via the OneToOne relation
        print(f"\nLibrarian for {library_name} library: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}' library.")


if __name__ == "__main__":
    # Example usage (you can adjust names to match your data)
    query_books_by_author("J.K. Rowling")
    list_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
