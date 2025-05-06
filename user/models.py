from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, unique=True)
    is_admin = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        super().save(*args, **kwargs)