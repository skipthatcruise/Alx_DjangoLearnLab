from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models



# Custom User Manager
class CustomUserManager(BaseUserManager):
    """Manager for CustomUser model"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize email (convert to lowercase)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with all required privileges"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='', null=True,blank=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    class Meta:
        permissions = [
            ("can_create", "can create book"),
            ("can_view", "can view book"),
            ("can_edit", "can edit book"),
            ("can_delete", "can delete book"),
        ]




