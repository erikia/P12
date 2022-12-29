from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    edition_date = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=7, choices=[("Admin", "Admin"), ("Sales", "Sales"),
                                                   ("Support", "Support")], null=True)
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return f"{self.username} - {self.role}"