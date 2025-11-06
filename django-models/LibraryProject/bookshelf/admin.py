from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Add filtering options on the right sidebar
    list_filter = ('author', 'publication_year')

    # Add search functionality for these fields
    search_fields = ('title', 'author')
# Register your models here.
