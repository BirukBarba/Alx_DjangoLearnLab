from django.shortcuts import render

# Create your views here.



# library/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book


@permission_required("library.can_view", raise_exception=True)
def book_list(request):
    """
    Shows all books.
    Requires: library.can_view
    """
    books = Book.objects.all()
    return render(request, "library/book_list.html", {"books": books})


@permission_required("library.can_create", raise_exception=True)
def book_create(request):
    """
    Creates a new book.
    Requires: library.can_create
    """
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objects.create(title=title, author=author)
        return redirect("book_list")

    return render(request, "library/book_create.html")


@permission_required("library.can_edit", raise_exception=True)
def book_edit(request, book_id):
    """
    Edits an existing book.
    Requires: library.can_edit
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.s
