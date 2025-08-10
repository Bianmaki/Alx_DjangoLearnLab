from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=150)