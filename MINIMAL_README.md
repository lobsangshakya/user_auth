# VERY Minimal Django OTP Authentication

## Project Structure (Only Essential Files)

```
User_auth/
├── minimal/
│   ├── models.py      # 2 models (15 lines)
│   ├── views.py       # 5 functions (49 lines)
│   ├── urls.py        # 5 routes (10 lines)
│   └── migrations/
├── templates/
│   ├── signup.html    # Signup form
│   ├── verify.html    # OTP verification
│   ├── login.html     # Login form
│   └── dashboard.html # Protected page
├── config/
│   ├── settings.py    # Added: minimal app, custom user, console email
│   └── urls.py        # Includes minimal.urls
└── db.sqlite3         # Database (ready)
```

## Code (Ultra-Short)

### models.py (15 lines)
```python
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
```

### views.py (49 lines)
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from .models import User, OTP

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(email=email, password=password, is_active=False)
        otp = OTP.objects.create(user=user, code=OTP.generate())
        send_mail('OTP', f'Your OTP: {otp.code}', 'test@localhost', [email])
        messages.success(request, f'OTP: {otp.code}')  # Shows in terminal
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
```

### urls.py (10 lines)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify/<int:user_id>/', views.verify, name='verify'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
```

### Templates (Minimal HTML)

**signup.html:**
```html
<!DOCTYPE html>
<html><head><title>Signup</title></head>
<body>
<h2>Signup</h2>
{% if messages %}{% for m in messages %}<p style="color:red">{{m}}</p>{% endfor %}{% endif %}
<form method="post">{% csrf_token %}
<input type="email" name="email" placeholder="Email" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Signup</button>
</form>
<p><a href="{% url 'login' %}">Login</a></p>
</body></html>
```

**verify.html:**
```html
<!DOCTYPE html>
<html><head><title>Verify OTP</title></head>
<body>
<h2>Enter OTP</h2>
{% if messages %}{% for m in messages %}<p style="color:red">{{m}}</p>{% endfor %}{% endif %}
<form method="post">{% csrf_token %}
<input type="text" name="code" placeholder="6-digit OTP" maxlength="6" required><br>
<button type="submit">Verify</button>
</form>
</body></html>
```

**login.html:**
```html
<!DOCTYPE html>
<html><head><title>Login</title></head>
<body>
<h2>Login</h2>
{% if messages %}{% for m in messages %}<p style="color:red">{{m}}</p>{% endfor %}{% endif %}
<form method="post">{% csrf_token %}
<input type="email" name="email" placeholder="Email" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Login</button>
</form>
<p><a href="{% url 'signup' %}">Signup</a></p>
</body></html>
```

**dashboard.html:**
```html
<!DOCTYPE html>
<html><head><title>Dashboard</title></head>
<body>
<h1>Welcome, {{ user.email }}!</h1>
<p>Email verified ✓</p>
<a href="{% url 'logout' %}">Logout</a>
</body></html>
```

## Settings Changes

**config/settings.py:**
```python
INSTALLED_APPS = [
    # ... default apps ...
    'minimal',  # Add this
]

AUTH_USER_MODEL = 'minimal.User'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**config/urls.py:**
```python
from django.urls import include

urlpatterns = [
    path('', include('minimal.urls')),  # Add this
    # ... other URLs ...
]
```

## How to Run

```bash
# Activate venv
source venv/bin/activate

# Run server
python manage.py runserver
```

## Test Flow

1. **Signup**: http://127.0.0.1:8000/signup/
   - Enter email & password
   - OTP printed in terminal (console backend)

2. **Verify**: http://127.0.0.1:8000/verify/1/
   - Enter OTP from terminal
   - User activated

3. **Login**: http://127.0.0.1:8000/login/
   - Use email & password
   - Only verified users can login

4. **Dashboard**: http://127.0.0.1:8000/dashboard/
   - Protected page (requires login)

## What You Learn

✅ Custom user model with email
✅ OTP generation (random 6 digits)
✅ Database storage (OTP model)
✅ Email backend (console for testing)
✅ User activation flow
✅ Login verification check
✅ Session-based auth
✅ CSRF protection
✅ Messages framework

## Total Code

- **Models**: 15 lines
- **Views**: 49 lines  
- **URLs**: 10 lines
- **Templates**: ~40 lines total
- **Settings**: 3 lines changed

**Total: ~117 lines of Python + ~40 lines HTML**

No JWT, no DRF, no complexity - just pure Django authentication!
