from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LibraryDetailView
from .views import list_books
from .views import register


urlpatterns = [
    # Function-based view for listing all libraries
    path('libraries/', list_books, name='list_books'),

    # Class-based view for displaying details of a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
