from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),  # default page
    path('verify/<int:user_id>/', views.verify, name='verify'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]