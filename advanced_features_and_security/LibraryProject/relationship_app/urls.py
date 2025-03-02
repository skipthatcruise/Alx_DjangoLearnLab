from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LibraryDetailView
from .views import list_books
from .import views
from .views import admin_view
from .views import librarian_view
from .views import member_view
from .views import add_book
from .views import edit_book
from .views import delete_book


urlpatterns = [
    # Function-based view for listing all libraries
    path('libraries/', list_books, name='list_books'),

    # Class-based view for displaying details of a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # URL to add a book (requires 'can_add_book' permission)
    path('add_book/', add_book, name='add_book'),

    # URL to edit a book (requires 'can_change_book' permission)
    path('edit_book/', edit_book, name='edit_book'),

    # URL to delete a book (requires 'can_delete_book' permission)
    path('delete_book/', delete_book, name='delete_book'),
]
