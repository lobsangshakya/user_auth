from django.shortcuts import render, redirect
from .models import OTP
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        print("Signup request received")
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        otp = OTP.objects.create(user=user, code=OTP.generate())
        print("OTP generated:", otp.code)
        print("Sending OTP email")
        
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp.code}',
                'lobsangshakya5@gmail.com', 
                [email],
                fail_silently=False
            )
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

        messages.success(request, f'OTP: {otp.code}')  # Show OTP in message for testing
        return redirect('verify', user.id)
    return render(request, 'signup.html')

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
            user.is_active = True
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
        user = authenticate(username=email, password=password)
        
        if user and user.is_active:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials or account not verified.')
    return render(request, 'login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
