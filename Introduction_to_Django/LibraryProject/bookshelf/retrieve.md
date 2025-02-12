from bookshelf.models import Book

python manage.py shell

retrieved_book = Book.objects.get(id=book.id)
#Title: 1984, Author: George Orwell