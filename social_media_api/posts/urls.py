from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Include the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]
