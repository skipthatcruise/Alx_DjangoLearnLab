import django
import os

# Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Replace 'your_project' with your actual project name
# django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f" - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

# 2️⃣ List all books in a specific library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # ManyToManyField relation
        print(f"Books in {library_name} Library:")
        for book in books:
            print(f" - {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

# 3️⃣ Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # OneToOneField relation
        print(f"The librarian for {library_name} is {librarian.name}.")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Librarian for '{library_name}' not found.")

# Test Queries
if __name__ == "__main__":
    get_books_by_author("J.K. Rowling")  # Change to an existing author in your database
    print("\n" + "="*30 + "\n")
    get_books_in_library("Central Library")  # Change to an existing library in your database
    print("\n" + "="*30 + "\n")
    get_librarian_for_library("Central Library")  # Change to an existing library
