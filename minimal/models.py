from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    
    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))
