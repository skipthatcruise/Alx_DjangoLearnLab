from django.urls import path
from.views import CustomBookListView, CustomBookCreateView, CustomBookDetailView, CustomBookDeleteView, CustomBookUpdateView

urlpatterns = [
    path('books/', CustomBookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', CustomBookDetailView.as_view(), name='book-detail'),
    path('books/create/', CustomBookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', CustomBookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', CustomBookDeleteView.as_view(), name='book-delete'),
]