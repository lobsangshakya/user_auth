from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("verify/", views.verify),
    path("login/", views.login),
]