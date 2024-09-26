from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('admin', 'Admin')])

    def __str__(self):
        return self.username