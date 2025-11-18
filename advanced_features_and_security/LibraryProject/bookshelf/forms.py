# bookshelf/forms.py
from django import forms
from .models import Book  # Assuming you're working with a Book model

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, help_text="Enter the book title")
    content = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter the content or description")
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Example validation for title
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        # Example validation for content
        if len(content) < 20:
            raise forms.ValidationError("Content must be at least 20 characters long.")
        return content
