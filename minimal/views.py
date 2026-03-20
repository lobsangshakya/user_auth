from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from .models import User, OTP

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(
    username=email,
    email=email,
    password=password,
    is_active=False
)
        otp = OTP.objects.create(user=user, code=OTP.generate())
        send_mail('OTP', f'Your OTP: {otp.code}', 'test@localhost', [email])
        messages.success(request, f'OTP: {otp.code}')  # Show OTP in message for testing
        return redirect('verify', user.id)
    return render(request, 'signup.html')

def verify(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        code = request.POST['code']
        otp = OTP.objects.filter(user=user, code=code).first()
        if otp:
            user.is_active = True
            user.is_verified = True
            user.save()
            otp.delete()
            messages.success(request, 'Verified! Please login.')
            return redirect('login')
        messages.error(request, 'Invalid OTP')
    return render(request, 'verify.html', {'user_id': user_id})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user and user.is_verified:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials or not verified')
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')
