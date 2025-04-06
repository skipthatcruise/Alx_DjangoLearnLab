from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import our custom views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Login and Logout using Django built-in views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logged_out.html'), name='logout'),

    # Custom registration and profile views
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.home, name='home'),
    # path('posts/', views.posts, name='posts'),

# List all blog posts
    path('post/', views.PostListView.as_view(), name='posts-list'),

    # Detail view of a single post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # Create a new post
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),

    # Edit an existing post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),

    # Delete an existing post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)