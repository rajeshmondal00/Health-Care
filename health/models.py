from django.db import models

## user registration
class Register_User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField(max_length=100)
    dob = models.DateField(max_length=10)
    pincode = models.CharField(max_length=6)
    email = models.EmailField(max_length=50 , primary_key=True,unique=True)
    phone =  models.CharField(max_length=12 ,unique=True)
    # otp = models.CharField(max_length=6)
    password = models.CharField(max_length=12)

# class Appointment(models.Model):
#     department = models.CharField(max_length=30)
#     doctor = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     phone = models.ForeignKey(Register_User,on_delete=models.CASCADE)

## generate auto user id and password
class Auto_generate(models.Model):
    email =  models.ForeignKey(Register_User, on_delete=models.CASCADE)
    auto_user_id = models.CharField(max_length=12)
    auto_password = models.CharField(max_length=12)

# from django.utils import timezone
# from datetime import timedelta
    # def is_valid(self):
    #     return timezone.now() < self.created_at + timedelta(minutes=10)  # OTP valid for 10 minutes
