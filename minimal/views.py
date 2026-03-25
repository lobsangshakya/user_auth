from django.shortcuts import render, redirect
from .models import OTP
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
import os

# ---------------- SIGNUP ----------------
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        # delete old OTPs
        OTP.objects.filter(user=user).delete()

        otp = OTP.objects.create(user=user, code=OTP.generate())

        try:
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is {otp.code}',
                from_email=os.environ.get("DEFAULT_FROM_EMAIL"),
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email.')

        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, "Failed to send OTP")

        return redirect('verify', user.id)

    return render(request, 'signup.html')


# ---------------- VERIFY ----------------
def verify(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('signup')

    if request.method == 'POST':
        code = request.POST['code']
        otp = OTP.objects.filter(user=user, code=code).first()

        if otp:
            if otp.is_valid():
                user.is_active = True
                user.save()
                otp.delete()
                messages.success(request, 'Verified! Please login.')
                return redirect('login')
            else:
                otp.delete()
                messages.error(request, 'OTP expired.')
        else:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'verify.html', {'user_id': user_id})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Account not verified.')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')


# ---------------- DASHBOARD ----------------
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')