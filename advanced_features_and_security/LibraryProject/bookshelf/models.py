from django.db import models
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
# Create your models here.


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser with email as required unique identifier."""

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending Django’s AbstractUser."""

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    # Replace default manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    








    from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    """
    Example model used to demonstrate custom permissions.
    Permissions added:
        - can_view
        - can_create
        - can_edit
        - can_delete
    """

    title = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        # Custom permissions
        permissions = [
            ("can_view", "Can view article"),
            ("can_create", "Can create article"),
            ("can_edit", "Can edit article"),
            ("can_delete", "Can delete article"),
        ]

    def __str__(self):
        return self.title