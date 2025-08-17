from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a sample book for testing
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2023
        )
        self.list_url = reverse("book-list")   # /books/
        self.detail_url = reverse("book-detail", args=[self.book.id])  # /books/<id>/

    def test_list_books(self):
        """Test retrieving the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # At least one book exists

    def test_retrieve_book(self):
        """Test retrieving a single book by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book(self):
        """Test creating a new book"""
        data = {"title": "New Book", "author": "New Author", "publication_year": 2024}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test updating an existing book"""
        data = {"title": "Updated Book", "author": "Updated Author", "publication_year": 2025}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        """Test deleting a book"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """Test filtering books by author"""
        response = self.client.get(self.list_url, {"author": "Test Author"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get(self.list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books(self):
        """Test ordering books by publication_year"""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
