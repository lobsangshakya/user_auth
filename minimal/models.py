from django.db import models
from django.contrib.auth.models import User
import random

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    
    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))
