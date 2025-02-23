from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LibraryDetailView
from .views import list_books
from .views import register
from .views import admin_view
from .views import librarian_view
from .views import member_view



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
]
