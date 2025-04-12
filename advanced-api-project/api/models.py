from django.db import models

class Author(models.Model): #The Author model is for storing the names of the Authors
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Book(models.Model): #The Book model is for storing details about the book which includes the title, publication year, and the author using ForeignKey
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title



