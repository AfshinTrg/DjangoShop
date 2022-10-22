from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.email}'

