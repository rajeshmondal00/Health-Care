from django.contrib import admin
from django.urls import path,include
from health import views
urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('forgotpassword/',views.forgot_password,name='forgot_password'),
    path('verify_otp/', views.verify_otp , name="verify_otp"),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin_dashboard/', views.admin_overview, name='admin_overview'),
    path('admin_dashboard/user_approval/', views.user_approval_dashboard, name='user_approval_dashboard'),
]

