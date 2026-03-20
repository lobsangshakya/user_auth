from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import OTP
import random

# Signup
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # create user (username required)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=False
        )

        code = str(random.randint(100000, 999999))
        OTP.objects.create(user=user, code=code)

        print("OTP:", code)  # console email

        return JsonResponse({"msg": "OTP sent"})
    
    return JsonResponse({"msg": "Invalid request"})


# Verify OTP
def verify(request):
    email = request.GET.get("email")
    code = request.GET.get("code")

    try:
        user = User.objects.get(email=email)
        otp = OTP.objects.get(user=user, code=code)

        user.is_active = True
        user.save()
        otp.delete()

        return JsonResponse({"msg": "Verified"})
    except:
        return JsonResponse({"msg": "Invalid OTP"})


# Login
def login(request):
    email = request.GET.get("email")
    password = request.GET.get("password")

    try:
        user = User.objects.get(email=email)

        if not user.check_password(password):
            return JsonResponse({"msg": "Wrong password"})

        if not user.is_active:
            return JsonResponse({"msg": "Verify first"})

        return JsonResponse({"msg": "Login success"})
    
    except:
        return JsonResponse({"msg": "User not found"})