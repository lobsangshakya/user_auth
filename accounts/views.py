from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import User, OTP
from datetime import datetime


def signup_view(request):
    """Handle user signup with email and password"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('signup')
        
        # Create user (inactive until verified)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False  # Deactivate until OTP verified
        )
        
        # Generate and send OTP
        otp_code = OTP.generate_otp()
        otp = OTP.objects.create(user=user, otp_code=otp_code)
        
        # Send email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp_code}. Valid for 5 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        messages.success(request, 'OTP sent to your email!')
        return redirect('verify_otp', user_id=user.id)
    
    return render(request, 'signup.html')


def verify_otp_view(request, user_id):
    """Verify OTP code entered by user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found!')
        return redirect('signup')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        
        # Find valid OTP
        otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
        
        if otp and otp.is_valid():
            # Activate user account
            user.is_active = True
            user.is_verified = True
            user.save()
            
            # Delete used OTP
            otp.delete()
            
            messages.success(request, 'Email verified successfully! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid or expired OTP!')
    
    return render(request, 'verify_otp.html', {'user_id': user_id})


def login_view(request):
    """Handle user login with email and password"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user:
            if user.is_verified:
                login(request, user)
                messages.success(request, f'Welcome, {user.email}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please verify your email first!')
        else:
            messages.error(request, 'Invalid email or password!')
    
    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    """Protected dashboard page - only for logged in users"""
    return render(request, 'dashboard.html')


def logout_view(request):
    """Handle user logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
