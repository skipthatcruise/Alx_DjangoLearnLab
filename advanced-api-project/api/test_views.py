# from django.test import TestCase
# from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.contrib.auth.models import User

class BookAPITest(APITestCase):
    def setUp(self):
        """Set up test data for the API"""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user) #Simulate Login
        self.author = Author.objects.create(name="J.K Rowling")
        self.book1 = Book.objects.create(title="Harry Potter", author=self.author, publication_year=2000)
        self.book2 = Book.objects.create(title="Fantastic Beasts", author=self.author, publication_year=2016)

        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/{self.book1.id}/update/"
        self.delete_url = f"/api/books/{self.book1.id}/delete/"

    # Test List Books (GET)
    def test_list_books(self):
        """Ensure books can be listed"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2) #Should return 2 books

    # Test Retrieve Single Book (GET)
    def test_retrieve_book(self):
        """Ensure a book can be retrieved"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Harry Potter")

    # Test Create Book (POST) - Requires Authentication
    def test_create_book_authenticated(self):
        """Ensure an authenticated user can create a book"""
        self.client.login(username="testuser", password="password")  # Authenticate
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2022,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot create a book"""
        data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "publication_year": 2022,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Update Book (PUT) - Requires Authentication
    def test_update_book_authenticated(self):
        """Ensure an authenticated user can update a book"""
        self.client.login(username="testuser", password="password")
        data = {
            "title": "Updated Book Title",
            "author": self.author.id,
            "publication_year": 2021,
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book Title")

    def test_update_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot update a book"""
        data = {
            "title": "Unauthorized Update",
            "author": self.author.id,
            "publication_year": 2021,
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Delete Book (DELETE) - Requires Authentication
    def test_delete_book_authenticated(self):
        """Ensure an authenticated user can delete a book"""
        self.client.login(username="testuser", password="password")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot delete a book"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Filtering, Searching & Ordering
    def test_filter_books(self):
        """Ensure filtering by title works"""
        response = self.client.get(f"{self.list_url}?title=Harry Potter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """Ensure searching by title works"""
        response = self.client.get(f"{self.list_url}?search=Harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Ensure ordering by publication_year works"""
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Harry Potter")  # Oldest first

        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Fantastic Beasts")  # Newest first




