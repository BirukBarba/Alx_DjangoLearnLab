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






# bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, help_text="Enter the book title")
    content = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter the content or description")
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError("Content must be at least 20 characters long.")
        return content





# bookshelf/views.py
from django.shortcuts import render
from .forms import ExampleForm  # <-- Correct Import

def book_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save it to the database or display it)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            return render(request, 'bookshelf/book_success.html', {'title': title, 'content': content})
        else:
            return render(request, 'bookshelf/form_example.html', {'form': form})
    else:
        form = ExampleForm()
        return render(request, 'bookshelf/form_example.html', {'form': form})
