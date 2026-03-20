from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from datetime import datetime, timedelta


class User(AbstractUser):
    """Custom user model with email as username"""
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # Track if email is verified
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class OTP(models.Model):
    """Store OTP codes for email verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # Auto-generate expiry time (5 minutes from now)
        if not self.expires_at:
            self.expires_at = datetime.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return datetime.now() < self.expires_at
    
    @staticmethod
    def generate_otp():
        """Generate a random 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
