from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books OR create a new one
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        if not title:
            raise ValueError("Title cannot be empty")
        serializer.save()

    # Allow read for everyone, but create only for authenticated users
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# Retrieve, update or delete a book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Auth required for update/delete, read-only open
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

