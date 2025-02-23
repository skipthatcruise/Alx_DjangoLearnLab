from django.urls import path
from .views import LibraryDetailView
from .views import list_books

urlpatterns = [
    # Function-based view for listing all libraries
    path('libraries/', library_list, name='library-list'),

    # Class-based view for displaying details of a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
