from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=150)

    class ExampleForm(forms.Form):
     """
      A simple example form for demonstrating CSRF protection and safe input handling.
     """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}),
        required=True
    )
