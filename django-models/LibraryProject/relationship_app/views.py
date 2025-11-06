from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library
from .models import Library
from django.views.generic.detail import DetailView

# --- Function-Based View ---
def list_books(request):
    """Display all books with their authors."""
    # Explicitly using Book.objects.all() as required
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# --- Class-Based View ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


# --- User Registration View ---
def register_view(request):
    """Allow new users to register."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            messages.success(request, "Registration successful!")
            return redirect('list_books')  # Redirect to a page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# --- User Login View ---
def login_view(request):
    """Allow existing users to log in."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('list_books')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# --- User Logout View ---
def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return render(request, 'relationship_app/logout.html')
