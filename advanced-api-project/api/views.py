from rest_framework import generics, serializers, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated




class CustomBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['title', 'author', 'publication_year']

    search_fields = ['title', 'author__name']

    ordering_fields = ['title', 'publication_year']

class CustomBookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.now().year

        if int(publication_year) > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")

        serializer.save()

class CustomBookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        publication_year = self.request.data.get("publication_year")
        current_year = datetime.now().year

        if int(publication_year) > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        serializer.save()

class CustomBookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
