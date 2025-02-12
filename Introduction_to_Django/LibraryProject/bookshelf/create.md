from bookshelf.models import Book

python manage.py shell

book = Book.object.create(
    title = '1984',
    author = 'George Orwell',
    publication_year = 1949
)
# The book has been created successfully
