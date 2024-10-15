from django.contrib import admin
from django.urls import path,include
from health import views
urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('login/', views.use_login,name='login'),
    path('register/',views.use_register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('forgotpassword/',views.forgot_password,name='forgot_password'),
    path('verify_otp/', views.verify_otp , name="verify_otp"),
]

