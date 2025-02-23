from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Library
from .models import Book
from .models import Author
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

# 🚀 View to Add a New Book (Requires "can_add_book" Permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')  # Redirect to book list after adding
    authors = Author.objects.all()  # Fetch all authors for selection
    return render(request, "relationship_app/add_book.html", {"authors": authors})

# 🚀 View to Edit a Book (Requires "can_change_book" Permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        if author_id:
            book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('list_books')  # Redirect to book list after editing
    authors = Author.objects.all()  # Fetch all authors for selection
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})

# 🚀 View to Delete a Book (Requires "can_delete_book" Permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')  # Redirect after successful deletion
    return render(request, "relationship_app/delete_book.html", {"book": book})



# Helper function to check roles
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin View
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian View
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member View
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# User Registration View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('list_books')  # Redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# Function-Based View (FBV) for Listing All Libraries
def list_books(request):
    libraries = Book.objects.all()  # Fetch all libraries from the database
    return render(request, "relationship_app/list_books.html", {"libraries": libraries})

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()  # Fetch all books related to this library
        return context
