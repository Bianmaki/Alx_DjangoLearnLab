from rest_framework import serializers
from .models import Author, Book
import datetime


# Serializer for Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    # Custom validation: ensure publication_year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for Author, including nested books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # nested serializer

    class Meta:
        model = Author
        fields = ["name", "books"]
