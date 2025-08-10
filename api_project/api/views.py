from rest_framework import generics
from .models import Book  # or from bookshelf.models import Book if it's in another app
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


